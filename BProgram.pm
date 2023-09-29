dtmc

formula is_HOT_requested = (is_bt_hot_requesting_HOT=true) | (is_bt_cold_requesting_HOT=true) | (is_add_random_requesting_HOT=true) | (is_interweave_requesting_HOT=true);
formula is_COLD_requested = (is_bt_hot_requesting_COLD=true) | (is_bt_cold_requesting_COLD=true) | (is_add_random_requesting_COLD=true) | (is_interweave_requesting_COLD=true);
formula is_X_requested = (is_bt_hot_requesting_X=true) | (is_bt_cold_requesting_X=true) | (is_add_random_requesting_X=true) | (is_interweave_requesting_X=true);
formula is_Y_requested = (is_bt_hot_requesting_Y=true) | (is_bt_cold_requesting_Y=true) | (is_add_random_requesting_Y=true) | (is_interweave_requesting_Y=true);

formula is_HOT_blocked = (is_bt_hot_blocking_HOT=true) | (is_bt_cold_blocking_HOT=true) | (is_add_random_blocking_HOT=true) | (is_interweave_blocking_HOT=true);
formula is_COLD_blocked = (is_bt_hot_blocking_COLD=true) | (is_bt_cold_blocking_COLD=true) | (is_add_random_blocking_COLD=true) | (is_interweave_blocking_COLD=true);
formula is_X_blocked = (is_bt_hot_blocking_X=true) | (is_bt_cold_blocking_X=true) | (is_add_random_blocking_X=true) | (is_interweave_blocking_X=true);
formula is_Y_blocked = (is_bt_hot_blocking_Y=true) | (is_bt_cold_blocking_Y=true) | (is_add_random_blocking_Y=true) | (is_interweave_blocking_Y=true);

formula is_HOT_selected = (is_HOT_requested=true) & (is_HOT_blocked=false);
formula is_COLD_selected = (is_COLD_requested=true) & (is_COLD_blocked=false);
formula is_X_selected = (is_X_requested=true) & (is_X_blocked=false);
formula is_Y_selected = (is_Y_requested=true) & (is_Y_blocked=false);

label "HOT" = (is_HOT_selected=true);
label "COLD" = (is_COLD_selected=true);
label "X" = (is_X_selected=true);
label "Y" = (is_Y_selected=true);
//-----------------------

formula is_bt_hot_requesting_HOT = (s_bt_hot=0);
formula is_bt_hot_requesting_COLD = false;
formula is_bt_hot_requesting_X = false;
formula is_bt_hot_requesting_Y = false;

formula is_bt_hot_blocking_HOT = false;
formula is_bt_hot_blocking_COLD = false;
formula is_bt_hot_blocking_X = false;
formula is_bt_hot_blocking_Y = false;
module bt_hot
	s_bt_hot: [0..0] init 0;

	[HOT] (s_bt_hot=0) & (is_HOT_selected=true) -> 1: (s_bt_hot'=0);
	[COLD] (s_bt_hot=0) & (is_COLD_selected=true) -> 1: (s_bt_hot'=0);
	[X] (s_bt_hot=0) & (is_X_selected=true) -> 1: (s_bt_hot'=0);
	[Y] (s_bt_hot=0) & (is_Y_selected=true) -> 1: (s_bt_hot'=0);
endmodule


formula is_bt_cold_requesting_HOT = false;
formula is_bt_cold_requesting_COLD = (s_bt_cold=0);
formula is_bt_cold_requesting_X = false;
formula is_bt_cold_requesting_Y = false;

formula is_bt_cold_blocking_HOT = false;
formula is_bt_cold_blocking_COLD = false;
formula is_bt_cold_blocking_X = false;
formula is_bt_cold_blocking_Y = false;
module bt_cold
	s_bt_cold: [0..0] init 0;

	[HOT] (s_bt_cold=0) & (is_HOT_selected=true) -> 1: (s_bt_cold'=0);
	[COLD] (s_bt_cold=0) & (is_COLD_selected=true) -> 1: (s_bt_cold'=0);
	[X] (s_bt_cold=0) & (is_X_selected=true) -> 1: (s_bt_cold'=0);
	[Y] (s_bt_cold=0) & (is_Y_selected=true) -> 1: (s_bt_cold'=0);
endmodule


formula is_add_random_requesting_HOT = false;
formula is_add_random_requesting_COLD = false;
formula is_add_random_requesting_X = (s_add_random=0);
formula is_add_random_requesting_Y = (s_add_random=0);

formula is_add_random_blocking_HOT = false;
formula is_add_random_blocking_COLD = false;
formula is_add_random_blocking_X = false;
formula is_add_random_blocking_Y = false;
module add_random
	s_add_random: [0..1] init 0;

	[HOT] (s_add_random=0) & (is_HOT_selected=true) -> 1: (s_add_random'=0);
	[COLD] (s_add_random=0) & (is_COLD_selected=true) -> 1: (s_add_random'=0);
	[X] (s_add_random=0) & (is_X_selected=true) -> 1: (s_add_random'=1);
	[Y] (s_add_random=0) & (is_Y_selected=true) -> 1: (s_add_random'=1);
	
	[HOT] (s_add_random=1) & (is_HOT_selected=true) -> 1: (s_add_random'=1);
	[COLD] (s_add_random=1) & (is_COLD_selected=true) -> 1: (s_add_random'=1);
	[X] (s_add_random=1) & (is_X_selected=true) -> 1: (s_add_random'=1);
	[Y] (s_add_random=1) & (is_Y_selected=true) -> 1: (s_add_random'=1);
endmodule


formula is_interweave_requesting_HOT = false;
formula is_interweave_requesting_COLD = false;
formula is_interweave_requesting_X = false;
formula is_interweave_requesting_Y = false;

formula is_interweave_blocking_HOT = (s_interweave=0);
formula is_interweave_blocking_COLD = (s_interweave=1);
formula is_interweave_blocking_X = false;
formula is_interweave_blocking_Y = (s_interweave=0);
module interweave
	s_interweave: [0..1] init 0;

	[HOT] (s_interweave=0) & (is_HOT_selected=true) -> 1: (s_interweave'=0);
	[COLD] (s_interweave=0) & (is_COLD_selected=true) -> 1: (s_interweave'=1);
	[X] (s_interweave=0) & (is_X_selected=true) -> 1: (s_interweave'=0);
	[Y] (s_interweave=0) & (is_Y_selected=true) -> 1: (s_interweave'=0);
	
	[HOT] (s_interweave=1) & (is_HOT_selected=true) -> 1: (s_interweave'=0);
	[COLD] (s_interweave=1) & (is_COLD_selected=true) -> 1: (s_interweave'=1);
	[X] (s_interweave=1) & (is_X_selected=true) -> 1: (s_interweave'=1);
	[Y] (s_interweave=1) & (is_Y_selected=true) -> 1: (s_interweave'=1);
endmodule
