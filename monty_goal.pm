dtmc

formula is_h_requested = (is_host_requesting_h=true) | (is_car_requesting_h=true) | (is_player_requesting_h=true);
formula is_g_requested = (is_host_requesting_g=true) | (is_car_requesting_g=true) | (is_player_requesting_g=true);
formula is_o1_requested = (is_host_requesting_o1=true) | (is_car_requesting_o1=true) | (is_player_requesting_o1=true);
formula is_o2_requested = (is_host_requesting_o2=true) | (is_car_requesting_o2=true) | (is_player_requesting_o2=true);
formula is_o3_requested = (is_host_requesting_o3=true) | (is_car_requesting_o3=true) | (is_player_requesting_o3=true);

formula is_h_blocked = (is_host_blocking_h=true) | (is_car_blocking_h=true) | (is_player_blocking_h=true);
formula is_g_blocked = (is_host_blocking_g=true) | (is_car_blocking_g=true) | (is_player_blocking_g=true);
formula is_o1_blocked = (is_host_blocking_o1=true) | (is_car_blocking_o1=true) | (is_player_blocking_o1=true);
formula is_o2_blocked = (is_host_blocking_o2=true) | (is_car_blocking_o2=true) | (is_player_blocking_o2=true);
formula is_o3_blocked = (is_host_blocking_o3=true) | (is_car_blocking_o3=true) | (is_player_blocking_o3=true);

formula is_h_selected = (is_h_requested=true) & (is_h_blocked=false);
formula is_g_selected = (is_g_requested=true) & (is_g_blocked=false);
formula is_o1_selected = (is_o1_requested=true) & (is_o1_blocked=false);
formula is_o2_selected = (is_o2_requested=true) & (is_o2_blocked=false);
formula is_o3_selected = (is_o3_requested=true) & (is_o3_blocked=false);

label "h" = (is_h_selected=true);
label "g" = (is_g_selected=true);
label "o1" = (is_o1_selected=true);
label "o2" = (is_o2_selected=true);
label "o3" = (is_o3_selected=true);
//-----------------------

formula is_host_requesting_h = (s_host=0);
formula is_host_requesting_g = (s_host=1);
formula is_host_requesting_o1 = (s_host=2);
formula is_host_requesting_o2 = (s_host=2);
formula is_host_requesting_o3 = (s_host=2);

formula is_host_blocking_h = false;
formula is_host_blocking_g = false;
formula is_host_blocking_o1 = false;
formula is_host_blocking_o2 = false;
formula is_host_blocking_o3 = false;
module host
	s_host: [0..3] init 0;

	[h] (s_host=0) & (is_h_selected=true) -> 1: (s_host'=1);
	[g] (s_host=0) & (is_g_selected=true) -> 1: (s_host'=0);
	[o1] (s_host=0) & (is_o1_selected=true) -> 1: (s_host'=0);
	[o2] (s_host=0) & (is_o2_selected=true) -> 1: (s_host'=0);
	[o3] (s_host=0) & (is_o3_selected=true) -> 1: (s_host'=0);
	
	[h] (s_host=1) & (is_h_selected=true) -> 1: (s_host'=1);
	[g] (s_host=1) & (is_g_selected=true) -> 1: (s_host'=2);
	[o1] (s_host=1) & (is_o1_selected=true) -> 1: (s_host'=1);
	[o2] (s_host=1) & (is_o2_selected=true) -> 1: (s_host'=1);
	[o3] (s_host=1) & (is_o3_selected=true) -> 1: (s_host'=1);
	
	[h] (s_host=2) & (is_h_selected=true) -> 1: (s_host'=2);
	[g] (s_host=2) & (is_g_selected=true) -> 1: (s_host'=2);
	[o1] (s_host=2) & (is_o1_selected=true) -> 1: (s_host'=3);
	[o2] (s_host=2) & (is_o2_selected=true) -> 1: (s_host'=3);
	[o3] (s_host=2) & (is_o3_selected=true) -> 1: (s_host'=3);
	
	[h] (s_host=3) & (is_h_selected=true) -> 1: (s_host'=3);
	[g] (s_host=3) & (is_g_selected=true) -> 1: (s_host'=3);
	[o1] (s_host=3) & (is_o1_selected=true) -> 1: (s_host'=3);
	[o2] (s_host=3) & (is_o2_selected=true) -> 1: (s_host'=3);
	[o3] (s_host=3) & (is_o3_selected=true) -> 1: (s_host'=3);
endmodule


formula is_car_requesting_h = false;
formula is_car_requesting_g = false;
formula is_car_requesting_o1 = false;
formula is_car_requesting_o2 = false;
formula is_car_requesting_o3 = false;

formula is_car_blocking_h = false;
formula is_car_blocking_g = false;
formula is_car_blocking_o1 = (s_car=3);
formula is_car_blocking_o2 = (s_car=2);
formula is_car_blocking_o3 = (s_car=1);
module car
	s_car: [0..3] init 0;

	[h] (s_car=0) & (is_h_selected=true) -> 1/3: (s_car'=1) + 1/3: (s_car'=2)+ 1/3: (s_car'=3);
	[g] (s_car=0) & (is_g_selected=true) -> 1: (s_car'=0);
	[o1] (s_car=0) & (is_o1_selected=true) -> 1: (s_car'=0);
	[o2] (s_car=0) & (is_o2_selected=true) -> 1: (s_car'=0);
	[o3] (s_car=0) & (is_o3_selected=true) -> 1: (s_car'=0);
	
	[h] (s_car=1) & (is_h_selected=true) -> 1: (s_car'=1);
	[g] (s_car=1) & (is_g_selected=true) -> 1: (s_car'=1);
	[o1] (s_car=1) & (is_o1_selected=true) -> 1: (s_car'=1);
	[o2] (s_car=1) & (is_o2_selected=true) -> 1: (s_car'=1);
	[o3] (s_car=1) & (is_o3_selected=true) -> 1: (s_car'=1);
	
	[h] (s_car=2) & (is_h_selected=true) -> 1: (s_car'=2);
	[g] (s_car=2) & (is_g_selected=true) -> 1: (s_car'=2);
	[o1] (s_car=2) & (is_o1_selected=true) -> 1: (s_car'=2);
	[o2] (s_car=2) & (is_o2_selected=true) -> 1: (s_car'=2);
	[o3] (s_car=2) & (is_o3_selected=true) -> 1: (s_car'=2);
	
	[h] (s_car=3) & (is_h_selected=true) -> 1: (s_car'=3);
	[g] (s_car=3) & (is_g_selected=true) -> 1: (s_car'=3);
	[o1] (s_car=3) & (is_o1_selected=true) -> 1: (s_car'=3);
	[o2] (s_car=3) & (is_o2_selected=true) -> 1: (s_car'=3);
	[o3] (s_car=3) & (is_o3_selected=true) -> 1: (s_car'=3);
endmodule


formula is_player_requesting_h = false;
formula is_player_requesting_g = false;
formula is_player_requesting_o1 = false;
formula is_player_requesting_o2 = false;
formula is_player_requesting_o3 = false;

formula is_player_blocking_h = false;
formula is_player_blocking_g = false;
formula is_player_blocking_o1 = (s_player=3);
formula is_player_blocking_o2 = (s_player=2);
formula is_player_blocking_o3 = (s_player=1);
module player
	s_player: [0..3] init 0;

	[h] (s_player=0) & (is_h_selected=true) -> 1: (s_player'=0);
	[g] (s_player=0) & (is_g_selected=true) -> 1/3: (s_player'=3) + 1/3: (s_player'=2) + 1/3: (s_player'=1);
	[o1] (s_player=0) & (is_o1_selected=true) -> 1: (s_player'=0);
	[o2] (s_player=0) & (is_o2_selected=true) -> 1: (s_player'=0);
	[o3] (s_player=0) & (is_o3_selected=true) -> 1: (s_player'=0);
	
	[h] (s_player=1) & (is_h_selected=true) -> 1: (s_player'=1);
	[g] (s_player=1) & (is_g_selected=true) -> 1: (s_player'=1);
	[o1] (s_player=1) & (is_o1_selected=true) -> 1: (s_player'=1);
	[o2] (s_player=1) & (is_o2_selected=true) -> 1: (s_player'=1);
	[o3] (s_player=1) & (is_o3_selected=true) -> 1: (s_player'=1);
	
	[h] (s_player=2) & (is_h_selected=true) -> 1: (s_player'=2);
	[g] (s_player=2) & (is_g_selected=true) -> 1: (s_player'=2);
	[o1] (s_player=2) & (is_o1_selected=true) -> 1: (s_player'=2);
	[o2] (s_player=2) & (is_o2_selected=true) -> 1: (s_player'=2);
	[o3] (s_player=2) & (is_o3_selected=true) -> 1: (s_player'=2);
	
	[h] (s_player=3) & (is_h_selected=true) -> 1: (s_player'=3);
	[g] (s_player=3) & (is_g_selected=true) -> 1: (s_player'=3);
	[o1] (s_player=3) & (is_o1_selected=true) -> 1: (s_player'=3);
	[o2] (s_player=3) & (is_o2_selected=true) -> 1: (s_player'=3);
	[o3] (s_player=3) & (is_o3_selected=true) -> 1: (s_player'=3);
endmodule
