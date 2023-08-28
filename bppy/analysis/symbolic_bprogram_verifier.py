from bppy.utils.dfs import DFSBThread
from bppy.model.sync_statement import request, block, waitFor
from bppy.model.b_event import BEvent
from bppy.model.event_selection.simple_event_selection_strategy import SimpleEventSelectionStrategy
import sys
import tempfile
try:
    import pynusmv
    from pynusmv.model import *
    from pynusmv.mc import check_ltl_spec, check_explain_ltl_spec
    from pynusmv.bmc.glob import bmc_setup, BmcSupport, master_be_fsm
    from pynusmv.parser import parse_ltl_spec
    from pynusmv.node import Node
    from pynusmv.sat import SatSolverFactory, Polarity, SatSolverResult
    from pynusmv.bmc import ltlspec, utils as bmcutils
except ImportError:
    raise ImportError("PyNuSMV is not installed. Please install it to use SymbolicBProgramVerifier. More info on "
                      "PyNuSMV installation can be found at https://github.com/LouvainVerificationLab/pynusmv")


class SymbolicBProgramVerifier:
    """
    A class to verify a behavioral program symbolically using `PyNuSMV`. The verifier can operate in two modes:
    Binary Decision Diagrams (BDD) and SAT-based Bounded Model Checking (BMC).

    *Note:*

    1. The class requires the installation of `PyNuSMV`. More info on its installation can be found at `https://github.com/LouvainVerificationLab/pynusmv
    <https://github.com/LouvainVerificationLab/pynusmv>`_.

    2. The verifier is currently limited to b-programs with :class:`SimpleEventSelectionStrategy
    <bppy.model.event_selection.event_selection_strategy.SimpleEventSelectionStrategy>`.

    3. The verifier does not support events with data.

    Attributes:
    -----------
    bprogram_generator : function
        A function that generates a new instance of the BProgram.
    event_list : list
        List of all possible events in the system.
    """
    def __init__(self, bprogram_generator, event_list):
        self.bprogram_generator = bprogram_generator
        self.event_list = event_list
        self.bthread_num = len(self.bprogram_generator().bthreads)
        sys.setrecursionlimit(10000)

    def verify(self, spec, type="BDD", bound=1000, find_counterexample=False, print_info=False):
        """
        Verifies a given specification against the behavioral program.

        Parameters:
        -----------
        spec : str
            The specification to be verified, in `NuSMV <https://nusmv.fbk.eu/>`_ LTL specification format.
        type : str, optional
            The verification type to be used: Binary Decision Diagrams ("BDD") or SAT-based Bounded Model Checking ("BMC").
            Default is "BDD".
        bound : int, optional
            For BMC, the maximum number of steps to be considered. Default is 1000.
        find_counterexample : bool, optional
            If True and a specification violation is found, a counterexample is produced.
            Default is False.
        print_info : bool, optional
            If True, information about the verification process is printed. Default is False.

        Returns:
        --------
        bool:
            True if the specification is satisfied, False otherwise.
        Optional[str]:
            A counterexample, if one exists and find_counterexample is True. Otherwise, None.
        """
        if print_info:
            print("initializing NuSMV")
        pynusmv.init.init_nusmv()
        if print_info:
            print("Converting bthreads to NuSMV modules")
        bt_list = []
        for i in range(self.bthread_num):
            bt_list.append(self._bthread_to_module(lambda: self.bprogram_generator().bthreads[i],
                                                   self.bprogram_generator().bthreads[i].__name__ + str(i),
                                                   self.event_list))
        if print_info:
            print("Creating main module")
        main = self._main_module(self.event_list, bt_list)
        if print_info:
            print("Loading model into NuSMV")

        temp_dir = tempfile.TemporaryDirectory()
        with open(temp_dir.name + "/bp_model.smv", "w") as f:
            for bt in bt_list:
                f.write(str(bt))
                f.write("\n")
            f.write(str(main))
            f.write("\n")
            f.write("LTLSPEC " + str(spec).strip())
        pynusmv.glob.load_from_file(temp_dir.name + "/bp_model.smv")

        if type == "BMC":
            if print_info:
                print("Computing model")
            pynusmv.glob.flatten_hierarchy()
            pynusmv.glob.encode_variables()
            pynusmv.glob.build_boolean_model()
            bmc_setup()
            spec = pynusmv.glob.prop_database()[0].expr
            if print_info:
                print("Checking LTL spec")
            with BmcSupport():
                fml = Node.from_ptr(parse_ltl_spec(str(spec).strip()))
                fsm = master_be_fsm()
                problem = ltlspec.generate_ltl_problem(fsm, fml, bound)
                fsm = master_be_fsm()
                cnf = problem.to_cnf(Polarity.POSITIVE)

                solver = SatSolverFactory.create()
                solver += cnf
                solver.polarity(cnf, Polarity.POSITIVE)
                solution = solver.solve()
                result = solution != SatSolverResult.SATISFIABLE

                if not result and find_counterexample:
                    if print_info:
                        print("Finding counterexample")
                    cnt_ex = bmcutils.generate_counter_example(fsm, problem, solver, bound, "Violation")
                    explanation_str = ""
                    first_loop_signal = False
                    for step in cnt_ex:
                        if step.is_loopback:
                            if first_loop_signal:
                                break
                            first_loop_signal = True
                            explanation_str += "-- Loop starts here" + "\n"
                        for symbol, value in step:
                            if str(symbol) == "event":
                                explanation_str += str(value) + "\n"
                else:
                    explanation_str = None
        elif type == "BDD":
            if print_info:
                print("Computing model")
            pynusmv.glob.compute_model()

            # spec = prop.ag(prop.af(prop.atom(("must_finish = FALSE"))))
            spec = pynusmv.glob.prop_database()[0].expr

            if print_info:
                print("Checking LTL spec")
            #fsm = pynusmv.glob.prop_database().master.bddFsm
            result = check_ltl_spec(spec)
            if not result and find_counterexample:
                if print_info:
                    print("Finding counterexample")
                _, explanation = check_explain_ltl_spec(spec)
                explanation_str = ""
                first_loop_signal = False
                for state in explanation[2:-1:2]:
                    if state == explanation[2::2][-1]:
                        if first_loop_signal:
                            break
                        first_loop_signal = True
                        explanation_str += "-- Loop starts here" + "\n"
                    explanation_str += state["event"] + "\n"
            else:
                explanation_str = None
        else:
            pynusmv.init.deinit_nusmv()
            temp_dir.cleanup()
            raise ValueError("Unknown type. Use 'BDD' or 'BMC'")

        pynusmv.init.deinit_nusmv()
        temp_dir.cleanup()
        return result, explanation_str

    def _bthread_to_module(self, bthread_generator, bthread_name, event_list):

        dfs = DFSBThread(bthread_generator, SimpleEventSelectionStrategy(), event_list)
        init_s, visited, requested, blocked = dfs.run(return_requested_and_blocked=True)

        visited = dict([(k, v) for k, v in enumerate(visited)])
        id_to_change = [k for k, v in visited.items() if v == init_s][0]
        s_to_change = visited[0]
        visited[id_to_change] = s_to_change
        visited[0] = init_s
        rev_visited = {v: k for k, v in visited.items()}

        bt1_mod_dict = {}
        bt1_mod_dict["event"] = Identifier("event")
        bt1_mod_dict["ARGS"] = [bt1_mod_dict["event"]]
        bt1_mod_dict["state"] = Var(Range(0, len(visited)))

        bt1_mod_dict.update({
            e.name + "_requested": Var(Boolean(), name=e.name + "_requested") for e in requested
        })
        bt1_mod_dict.update({
            e.name + "_blocked": Var(Boolean(), name=e.name + "_blocked") for e in blocked
        })
        # bt1_mod_dict["must_finish"] = Var(Boolean())
        bt1_mod_dict["INIT"] = [bt1_mod_dict["state"] == 0]
        bt1_mod_dict_assign = {}
        for e in requested:
            case_list = []
            for i, node in visited.items():
                if isinstance(node.data.get(request, {}), BEvent):
                    if e == node.data.get(request, {}):
                        case_list.append((bt1_mod_dict["state"] == i, Trueexp()))
                    else:
                        case_list.append((bt1_mod_dict["state"] == i, Falseexp()))
                else:
                    if e in node.data.get(request, {}):
                        case_list.append((bt1_mod_dict["state"] == i, Trueexp()))
                    else:
                        case_list.append((bt1_mod_dict["state"] == i, Falseexp()))
            case_list = tuple(case_list)
            bt1_mod_dict_assign[e.name + "_requested"] = Case(case_list + ((Trueexp(), Falseexp()),))
        for e in blocked:
            case_list = []
            for i, node in visited.items():
                if isinstance(node.data.get(block, {}), BEvent):
                    if e == node.data.get(block, {}):
                        case_list.append((bt1_mod_dict["state"] == i, Trueexp()))
                    else:
                        case_list.append((bt1_mod_dict["state"] == i, Falseexp()))
                else:
                    if e in node.data.get(block, {}):
                        case_list.append((bt1_mod_dict["state"] == i, Trueexp()))
                    else:
                        case_list.append((bt1_mod_dict["state"] == i, Falseexp()))
            case_list = tuple(case_list)
            bt1_mod_dict_assign[e.name + "_blocked"] = Case(case_list + ((Trueexp(), Falseexp()),))

        case_list = []
        for i, node in visited.items():
            d = {}
            for e, next_node in node.transitions.items():
                d[rev_visited[next_node]] = d.get(rev_visited[next_node], []) + [e]
            for j, events in d.items():
                if i == j:
                    continue  # self loop not necessary
                or_chain = Falseexp()
                for e in events:
                    or_chain = Or(bt1_mod_dict["event"].next() == e.name, or_chain)
                case_list.append((And(bt1_mod_dict["state"] == i, or_chain), j))
        bt1_mod_dict_assign["next(state)"] = Case(tuple(case_list) + ((Trueexp(), bt1_mod_dict["state"]),))
        # true_set = set([i for i, node in visited.items() if node.must_finish])
        # true_or_chain = Falseexp()
        # false_or_chain = Falseexp()
        # for i, node in visited.items():
        #     if i in true_set:
        #         true_or_chain = Or(bt1_mod_dict["state"] == i, true_or_chain)
        #     else:
        #         false_or_chain = Or(bt1_mod_dict["state"] == i, false_or_chain)
        # bt1_mod_dict_assign["must_finish"] = Case(((true_or_chain, Trueexp()),
        #                                            (false_or_chain, Falseexp()),
        #                                            (Trueexp(), Falseexp())))
        bt1_mod_dict["ASSIGN"] = bt1_mod_dict_assign
        return type(bthread_name, (Module,), bt1_mod_dict)

    def _main_module(self, event_list, bt_list):
        mod_dict = {}
        mod_dict["event"] = Var(Scalar(tuple(["BPROGRAM_START", "BPROGRAM_DONE"] + [x.name for x in event_list])))
        bt_modules = []
        for i, bt in enumerate(bt_list):
            mod_dict["bt" + str(i)] = Var(bt(mod_dict["event"]))
            bt_modules.append(mod_dict["bt" + str(i)])
        mod_dict["INIT"] = [mod_dict["event"] == "BPROGRAM_START"]
        mod_dict_define = {}
        for e in event_list:
            mod_dict_define[e.name + "_requested"] = Falseexp()
            mod_dict_define[e.name + "_blocked"] = Falseexp()
        all_requested = set()
        all_blocked = set()
        for i in range(len(bt_list)):
            for v in mod_dict["bt" + str(i)].type.VAR:
                if v.name in mod_dict_define:
                    if v.name.endswith("_requested"):
                        all_requested.add(v.name)
                    elif v.name.endswith("_blocked"):
                        all_blocked.add(v.name)
                    mod_dict_define[v.name] = Or("bt" + str(i) + "." + v.name, mod_dict_define[v.name])
        # mod_dict_define["must_finish"] = Falseexp()
        # for i in range(len(bt_list)):
        #     mod_dict_define["must_finish"] = Or("bt" + str(i) + ".must_finish", mod_dict_define["must_finish"])
        for e in event_list:
            mod_dict_define[e.name + "_enabled"] = And(e.name + "_requested", "!" + e.name + "_blocked")
        mod_dict["DEFINE"] = mod_dict_define
        trans_statement = NotEqual("next(event)", "BPROGRAM_START")
        any_enabled = Falseexp()
        for e in event_list:
            trans_statement = And(trans_statement, Implies("!" + e.name + "_enabled", NotEqual("next(event)", e.name)))
            any_enabled = Or(any_enabled, e.name + "_enabled")
        trans_statement = And(trans_statement, Implies(any_enabled, NotEqual("next(event)", "BPROGRAM_DONE")))
        trans_statement = And(trans_statement, Implies(Equal("event", "BPROGRAM_DONE"), Equal("next(event)", "BPROGRAM_DONE")))
        mod_dict["TRANS"] = [trans_statement]
        return type("main", (Module,), mod_dict)
