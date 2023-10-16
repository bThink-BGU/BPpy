request = "request"
waitFor = "waitFor"
block = "block"
mustFinish = "mustFinish"
priority = "priority"
localReward = "localReward"


class sync(dict):
    def __init__(self, *, request=None, waitFor=None, block=None, mustFinish=None, priority=None, localReward=None, **kwargs):
        if request is not None:
            self["request"] = request
        if waitFor is not None:
            self["waitFor"] = waitFor
        if block is not None:
            self["block"] = block
        if mustFinish is not None:
            self["mustFinish"] = mustFinish
        if priority is not None:
            self["priority"] = priority
        if localReward is not None:
            self["localReward"] = localReward
        super().__init__(kwargs)