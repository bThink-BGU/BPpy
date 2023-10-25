mdp

formula is_h1_requested = (is_host_requesting_h1=true) | (is_car_requesting_h1=true) | (is_guest_requesting_h1=true);
formula is_h2_requested = (is_host_requesting_h2=true) | (is_car_requesting_h2=true) | (is_guest_requesting_h2=true);
formula is_h3_requested = (is_host_requesting_h3=true) | (is_car_requesting_h3=true) | (is_guest_requesting_h3=true);
formula is_g1_requested = (is_host_requesting_g1=true) | (is_car_requesting_g1=true) | (is_guest_requesting_g1=true);
formula is_g2_requested = (is_host_requesting_g2=true) | (is_car_requesting_g2=true) | (is_guest_requesting_g2=true);
formula is_g3_requested = (is_host_requesting_g3=true) | (is_car_requesting_g3=true) | (is_guest_requesting_g3=true);
formula is_o1_requested = (is_host_requesting_o1=true) | (is_car_requesting_o1=true) | (is_guest_requesting_o1=true);
formula is_o2_requested = (is_host_requesting_o2=true) | (is_car_requesting_o2=true) | (is_guest_requesting_o2=true);
formula is_o3_requested = (is_host_requesting_o3=true) | (is_car_requesting_o3=true) | (is_guest_requesting_o3=true);

formula is_h1_blocked = (is_host_blocking_h1=true) | (is_car_blocking_h1=true) | (is_guest_blocking_h1=true);
formula is_h2_blocked = (is_host_blocking_h2=true) | (is_car_blocking_h2=true) | (is_guest_blocking_h2=true);
formula is_h3_blocked = (is_host_blocking_h3=true) | (is_car_blocking_h3=true) | (is_guest_blocking_h3=true);
formula is_g1_blocked = (is_host_blocking_g1=true) | (is_car_blocking_g1=true) | (is_guest_blocking_g1=true);
formula is_g2_blocked = (is_host_blocking_g2=true) | (is_car_blocking_g2=true) | (is_guest_blocking_g2=true);
formula is_g3_blocked = (is_host_blocking_g3=true) | (is_car_blocking_g3=true) | (is_guest_blocking_g3=true);
formula is_o1_blocked = (is_host_blocking_o1=true) | (is_car_blocking_o1=true) | (is_guest_blocking_o1=true);
formula is_o2_blocked = (is_host_blocking_o2=true) | (is_car_blocking_o2=true) | (is_guest_blocking_o2=true);
formula is_o3_blocked = (is_host_blocking_o3=true) | (is_car_blocking_o3=true) | (is_guest_blocking_o3=true);

formula is_h1_selected = (is_h1_requested=true) & (is_h1_blocked=false);
formula is_h2_selected = (is_h2_requested=true) & (is_h2_blocked=false);
formula is_h3_selected = (is_h3_requested=true) & (is_h3_blocked=false);
formula is_g1_selected = (is_g1_requested=true) & (is_g1_blocked=false);
formula is_g2_selected = (is_g2_requested=true) & (is_g2_blocked=false);
formula is_g3_selected = (is_g3_requested=true) & (is_g3_blocked=false);
formula is_o1_selected = (is_o1_requested=true) & (is_o1_blocked=false);
formula is_o2_selected = (is_o2_requested=true) & (is_o2_blocked=false);
formula is_o3_selected = (is_o3_requested=true) & (is_o3_blocked=false);

label "h1" = (is_h1_selected=true);
label "h2" = (is_h2_selected=true);
label "h3" = (is_h3_selected=true);
label "g1" = (is_g1_selected=true);
label "g2" = (is_g2_selected=true);
label "g3" = (is_g3_selected=true);
label "o1" = (is_o1_selected=true);
label "o2" = (is_o2_selected=true);
label "o3" = (is_o3_selected=true);
//-----------------------

formula is_host_requesting_h1 = (s_host=12);
formula is_host_requesting_h2 = (s_host=7);
formula is_host_requesting_h3 = (s_host=1);
formula is_host_requesting_g1 = (s_host=6) | (s_host=11) | (s_host=16);
formula is_host_requesting_g2 = (s_host=5) | (s_host=10) | (s_host=15);
formula is_host_requesting_g3 = (s_host=3) | (s_host=9) | (s_host=14);
formula is_host_requesting_o1 = false;
formula is_host_requesting_o2 = false;
formula is_host_requesting_o3 = false;

formula is_host_blocking_h1 = false;
formula is_host_blocking_h2 = false;
formula is_host_blocking_h3 = false;
formula is_host_blocking_g1 = false;
formula is_host_blocking_g2 = false;
formula is_host_blocking_g3 = false;
formula is_host_blocking_o1 = false;
formula is_host_blocking_o2 = false;
formula is_host_blocking_o3 = false;
module host
	s_host: [0..16] init 0;

	[h1] (s_host=1) & (is_h1_selected=true) -> 1: (s_host'=1);
	[h2] (s_host=1) & (is_h2_selected=true) -> 1: (s_host'=1);
	[h3] (s_host=1) & (is_h3_selected=true) -> 1: (s_host'=2);
	[g1] (s_host=1) & (is_g1_selected=true) -> 1: (s_host'=1);
	[g2] (s_host=1) & (is_g2_selected=true) -> 1: (s_host'=1);
	[g3] (s_host=1) & (is_g3_selected=true) -> 1: (s_host'=1);
	[o1] (s_host=1) & (is_o1_selected=true) -> 1: (s_host'=1);
	[o2] (s_host=1) & (is_o2_selected=true) -> 1: (s_host'=1);
	[o3] (s_host=1) & (is_o3_selected=true) -> 1: (s_host'=1);
	
	[h1] (s_host=3) & (is_h1_selected=true) -> 1: (s_host'=3);
	[h2] (s_host=3) & (is_h2_selected=true) -> 1: (s_host'=3);
	[h3] (s_host=3) & (is_h3_selected=true) -> 1: (s_host'=3);
	[g1] (s_host=3) & (is_g1_selected=true) -> 1: (s_host'=3);
	[g2] (s_host=3) & (is_g2_selected=true) -> 1: (s_host'=3);
	[g3] (s_host=3) & (is_g3_selected=true) -> 1: (s_host'=4);
	[o1] (s_host=3) & (is_o1_selected=true) -> 1: (s_host'=3);
	[o2] (s_host=3) & (is_o2_selected=true) -> 1: (s_host'=3);
	[o3] (s_host=3) & (is_o3_selected=true) -> 1: (s_host'=3);
	
	[h1] (s_host=5) & (is_h1_selected=true) -> 1: (s_host'=5);
	[h2] (s_host=5) & (is_h2_selected=true) -> 1: (s_host'=5);
	[h3] (s_host=5) & (is_h3_selected=true) -> 1: (s_host'=5);
	[g1] (s_host=5) & (is_g1_selected=true) -> 1: (s_host'=5);
	[g2] (s_host=5) & (is_g2_selected=true) -> 1: (s_host'=4);
	[g3] (s_host=5) & (is_g3_selected=true) -> 1: (s_host'=5);
	[o1] (s_host=5) & (is_o1_selected=true) -> 1: (s_host'=5);
	[o2] (s_host=5) & (is_o2_selected=true) -> 1: (s_host'=5);
	[o3] (s_host=5) & (is_o3_selected=true) -> 1: (s_host'=5);
	
	[h1] (s_host=6) & (is_h1_selected=true) -> 1: (s_host'=6);
	[h2] (s_host=6) & (is_h2_selected=true) -> 1: (s_host'=6);
	[h3] (s_host=6) & (is_h3_selected=true) -> 1: (s_host'=6);
	[g1] (s_host=6) & (is_g1_selected=true) -> 1: (s_host'=4);
	[g2] (s_host=6) & (is_g2_selected=true) -> 1: (s_host'=6);
	[g3] (s_host=6) & (is_g3_selected=true) -> 1: (s_host'=6);
	[o1] (s_host=6) & (is_o1_selected=true) -> 1: (s_host'=6);
	[o2] (s_host=6) & (is_o2_selected=true) -> 1: (s_host'=6);
	[o3] (s_host=6) & (is_o3_selected=true) -> 1: (s_host'=6);
	
	[h1] (s_host=7) & (is_h1_selected=true) -> 1: (s_host'=7);
	[h2] (s_host=7) & (is_h2_selected=true) -> 1: (s_host'=8);
	[h3] (s_host=7) & (is_h3_selected=true) -> 1: (s_host'=7);
	[g1] (s_host=7) & (is_g1_selected=true) -> 1: (s_host'=7);
	[g2] (s_host=7) & (is_g2_selected=true) -> 1: (s_host'=7);
	[g3] (s_host=7) & (is_g3_selected=true) -> 1: (s_host'=7);
	[o1] (s_host=7) & (is_o1_selected=true) -> 1: (s_host'=7);
	[o2] (s_host=7) & (is_o2_selected=true) -> 1: (s_host'=7);
	[o3] (s_host=7) & (is_o3_selected=true) -> 1: (s_host'=7);
	
	[h1] (s_host=9) & (is_h1_selected=true) -> 1: (s_host'=9);
	[h2] (s_host=9) & (is_h2_selected=true) -> 1: (s_host'=9);
	[h3] (s_host=9) & (is_h3_selected=true) -> 1: (s_host'=9);
	[g1] (s_host=9) & (is_g1_selected=true) -> 1: (s_host'=9);
	[g2] (s_host=9) & (is_g2_selected=true) -> 1: (s_host'=9);
	[g3] (s_host=9) & (is_g3_selected=true) -> 1: (s_host'=4);
	[o1] (s_host=9) & (is_o1_selected=true) -> 1: (s_host'=9);
	[o2] (s_host=9) & (is_o2_selected=true) -> 1: (s_host'=9);
	[o3] (s_host=9) & (is_o3_selected=true) -> 1: (s_host'=9);
	
	[h1] (s_host=10) & (is_h1_selected=true) -> 1: (s_host'=10);
	[h2] (s_host=10) & (is_h2_selected=true) -> 1: (s_host'=10);
	[h3] (s_host=10) & (is_h3_selected=true) -> 1: (s_host'=10);
	[g1] (s_host=10) & (is_g1_selected=true) -> 1: (s_host'=10);
	[g2] (s_host=10) & (is_g2_selected=true) -> 1: (s_host'=4);
	[g3] (s_host=10) & (is_g3_selected=true) -> 1: (s_host'=10);
	[o1] (s_host=10) & (is_o1_selected=true) -> 1: (s_host'=10);
	[o2] (s_host=10) & (is_o2_selected=true) -> 1: (s_host'=10);
	[o3] (s_host=10) & (is_o3_selected=true) -> 1: (s_host'=10);
	
	[h1] (s_host=11) & (is_h1_selected=true) -> 1: (s_host'=11);
	[h2] (s_host=11) & (is_h2_selected=true) -> 1: (s_host'=11);
	[h3] (s_host=11) & (is_h3_selected=true) -> 1: (s_host'=11);
	[g1] (s_host=11) & (is_g1_selected=true) -> 1: (s_host'=4);
	[g2] (s_host=11) & (is_g2_selected=true) -> 1: (s_host'=11);
	[g3] (s_host=11) & (is_g3_selected=true) -> 1: (s_host'=11);
	[o1] (s_host=11) & (is_o1_selected=true) -> 1: (s_host'=11);
	[o2] (s_host=11) & (is_o2_selected=true) -> 1: (s_host'=11);
	[o3] (s_host=11) & (is_o3_selected=true) -> 1: (s_host'=11);
	
	[h1] (s_host=12) & (is_h1_selected=true) -> 1: (s_host'=13);
	[h2] (s_host=12) & (is_h2_selected=true) -> 1: (s_host'=12);
	[h3] (s_host=12) & (is_h3_selected=true) -> 1: (s_host'=12);
	[g1] (s_host=12) & (is_g1_selected=true) -> 1: (s_host'=12);
	[g2] (s_host=12) & (is_g2_selected=true) -> 1: (s_host'=12);
	[g3] (s_host=12) & (is_g3_selected=true) -> 1: (s_host'=12);
	[o1] (s_host=12) & (is_o1_selected=true) -> 1: (s_host'=12);
	[o2] (s_host=12) & (is_o2_selected=true) -> 1: (s_host'=12);
	[o3] (s_host=12) & (is_o3_selected=true) -> 1: (s_host'=12);
	
	[h1] (s_host=14) & (is_h1_selected=true) -> 1: (s_host'=14);
	[h2] (s_host=14) & (is_h2_selected=true) -> 1: (s_host'=14);
	[h3] (s_host=14) & (is_h3_selected=true) -> 1: (s_host'=14);
	[g1] (s_host=14) & (is_g1_selected=true) -> 1: (s_host'=14);
	[g2] (s_host=14) & (is_g2_selected=true) -> 1: (s_host'=14);
	[g3] (s_host=14) & (is_g3_selected=true) -> 1: (s_host'=4);
	[o1] (s_host=14) & (is_o1_selected=true) -> 1: (s_host'=14);
	[o2] (s_host=14) & (is_o2_selected=true) -> 1: (s_host'=14);
	[o3] (s_host=14) & (is_o3_selected=true) -> 1: (s_host'=14);
	
	[h1] (s_host=15) & (is_h1_selected=true) -> 1: (s_host'=15);
	[h2] (s_host=15) & (is_h2_selected=true) -> 1: (s_host'=15);
	[h3] (s_host=15) & (is_h3_selected=true) -> 1: (s_host'=15);
	[g1] (s_host=15) & (is_g1_selected=true) -> 1: (s_host'=15);
	[g2] (s_host=15) & (is_g2_selected=true) -> 1: (s_host'=4);
	[g3] (s_host=15) & (is_g3_selected=true) -> 1: (s_host'=15);
	[o1] (s_host=15) & (is_o1_selected=true) -> 1: (s_host'=15);
	[o2] (s_host=15) & (is_o2_selected=true) -> 1: (s_host'=15);
	[o3] (s_host=15) & (is_o3_selected=true) -> 1: (s_host'=15);
	
	[h1] (s_host=16) & (is_h1_selected=true) -> 1: (s_host'=16);
	[h2] (s_host=16) & (is_h2_selected=true) -> 1: (s_host'=16);
	[h3] (s_host=16) & (is_h3_selected=true) -> 1: (s_host'=16);
	[g1] (s_host=16) & (is_g1_selected=true) -> 1: (s_host'=4);
	[g2] (s_host=16) & (is_g2_selected=true) -> 1: (s_host'=16);
	[g3] (s_host=16) & (is_g3_selected=true) -> 1: (s_host'=16);
	[o1] (s_host=16) & (is_o1_selected=true) -> 1: (s_host'=16);
	[o2] (s_host=16) & (is_o2_selected=true) -> 1: (s_host'=16);
	[o3] (s_host=16) & (is_o3_selected=true) -> 1: (s_host'=16);
	
	[] (s_host=0) -> 0.33: (s_host'=12) + 0.33: (s_host'=7) + 0.33: (s_host'=1);
	
	[] (s_host=2) -> 0.33: (s_host'=6) + 0.33: (s_host'=5) + 0.33: (s_host'=3);
	
	[] (s_host=8) -> 0.33: (s_host'=11) + 0.33: (s_host'=10) + 0.33: (s_host'=9);
	
	[] (s_host=13) -> 0.33: (s_host'=16) + 0.33: (s_host'=15) + 0.33: (s_host'=14);
endmodule


formula is_car_requesting_h1 = false;
formula is_car_requesting_h2 = false;
formula is_car_requesting_h3 = false;
formula is_car_requesting_g1 = false;
formula is_car_requesting_g2 = false;
formula is_car_requesting_g3 = false;
formula is_car_requesting_o1 = false;
formula is_car_requesting_o2 = false;
formula is_car_requesting_o3 = false;

formula is_car_blocking_h1 = false;
formula is_car_blocking_h2 = false;
formula is_car_blocking_h3 = false;
formula is_car_blocking_g1 = false;
formula is_car_blocking_g2 = false;
formula is_car_blocking_g3 = false;
formula is_car_blocking_o1 = (s_car=3);
formula is_car_blocking_o2 = (s_car=2);
formula is_car_blocking_o3 = (s_car=1);
module car
	s_car: [0..3] init 0;

	[h1] (s_car=0) & (is_h1_selected=true) -> 1: (s_car'=3);
	[h2] (s_car=0) & (is_h2_selected=true) -> 1: (s_car'=2);
	[h3] (s_car=0) & (is_h3_selected=true) -> 1: (s_car'=1);
	[g1] (s_car=0) & (is_g1_selected=true) -> 1: (s_car'=0);
	[g2] (s_car=0) & (is_g2_selected=true) -> 1: (s_car'=0);
	[g3] (s_car=0) & (is_g3_selected=true) -> 1: (s_car'=0);
	[o1] (s_car=0) & (is_o1_selected=true) -> 1: (s_car'=0);
	[o2] (s_car=0) & (is_o2_selected=true) -> 1: (s_car'=0);
	[o3] (s_car=0) & (is_o3_selected=true) -> 1: (s_car'=0);
	
	[h1] (s_car=1) & (is_h1_selected=true) -> 1: (s_car'=1);
	[h2] (s_car=1) & (is_h2_selected=true) -> 1: (s_car'=1);
	[h3] (s_car=1) & (is_h3_selected=true) -> 1: (s_car'=1);
	[g1] (s_car=1) & (is_g1_selected=true) -> 1: (s_car'=1);
	[g2] (s_car=1) & (is_g2_selected=true) -> 1: (s_car'=1);
	[g3] (s_car=1) & (is_g3_selected=true) -> 1: (s_car'=1);
	[o1] (s_car=1) & (is_o1_selected=true) -> 1: (s_car'=1);
	[o2] (s_car=1) & (is_o2_selected=true) -> 1: (s_car'=1);
	[o3] (s_car=1) & (is_o3_selected=true) -> 1: (s_car'=1);
	
	[h1] (s_car=2) & (is_h1_selected=true) -> 1: (s_car'=2);
	[h2] (s_car=2) & (is_h2_selected=true) -> 1: (s_car'=2);
	[h3] (s_car=2) & (is_h3_selected=true) -> 1: (s_car'=2);
	[g1] (s_car=2) & (is_g1_selected=true) -> 1: (s_car'=2);
	[g2] (s_car=2) & (is_g2_selected=true) -> 1: (s_car'=2);
	[g3] (s_car=2) & (is_g3_selected=true) -> 1: (s_car'=2);
	[o1] (s_car=2) & (is_o1_selected=true) -> 1: (s_car'=2);
	[o2] (s_car=2) & (is_o2_selected=true) -> 1: (s_car'=2);
	[o3] (s_car=2) & (is_o3_selected=true) -> 1: (s_car'=2);
	
	[h1] (s_car=3) & (is_h1_selected=true) -> 1: (s_car'=3);
	[h2] (s_car=3) & (is_h2_selected=true) -> 1: (s_car'=3);
	[h3] (s_car=3) & (is_h3_selected=true) -> 1: (s_car'=3);
	[g1] (s_car=3) & (is_g1_selected=true) -> 1: (s_car'=3);
	[g2] (s_car=3) & (is_g2_selected=true) -> 1: (s_car'=3);
	[g3] (s_car=3) & (is_g3_selected=true) -> 1: (s_car'=3);
	[o1] (s_car=3) & (is_o1_selected=true) -> 1: (s_car'=3);
	[o2] (s_car=3) & (is_o2_selected=true) -> 1: (s_car'=3);
	[o3] (s_car=3) & (is_o3_selected=true) -> 1: (s_car'=3);
endmodule


formula is_guest_requesting_h1 = false;
formula is_guest_requesting_h2 = false;
formula is_guest_requesting_h3 = false;
formula is_guest_requesting_g1 = false;
formula is_guest_requesting_g2 = false;
formula is_guest_requesting_g3 = false;
formula is_guest_requesting_o1 = false;
formula is_guest_requesting_o2 = false;
formula is_guest_requesting_o3 = false;

formula is_guest_blocking_h1 = false;
formula is_guest_blocking_h2 = false;
formula is_guest_blocking_h3 = false;
formula is_guest_blocking_g1 = false;
formula is_guest_blocking_g2 = false;
formula is_guest_blocking_g3 = false;
formula is_guest_blocking_o1 = (s_guest=3);
formula is_guest_blocking_o2 = (s_guest=2);
formula is_guest_blocking_o3 = (s_guest=1);
module guest
	s_guest: [0..3] init 0;

	[h1] (s_guest=0) & (is_h1_selected=true) -> 1: (s_guest'=0);
	[h2] (s_guest=0) & (is_h2_selected=true) -> 1: (s_guest'=0);
	[h3] (s_guest=0) & (is_h3_selected=true) -> 1: (s_guest'=0);
	[g1] (s_guest=0) & (is_g1_selected=true) -> 1: (s_guest'=3);
	[g2] (s_guest=0) & (is_g2_selected=true) -> 1: (s_guest'=2);
	[g3] (s_guest=0) & (is_g3_selected=true) -> 1: (s_guest'=1);
	[o1] (s_guest=0) & (is_o1_selected=true) -> 1: (s_guest'=0);
	[o2] (s_guest=0) & (is_o2_selected=true) -> 1: (s_guest'=0);
	[o3] (s_guest=0) & (is_o3_selected=true) -> 1: (s_guest'=0);
	
	[h1] (s_guest=1) & (is_h1_selected=true) -> 1: (s_guest'=1);
	[h2] (s_guest=1) & (is_h2_selected=true) -> 1: (s_guest'=1);
	[h3] (s_guest=1) & (is_h3_selected=true) -> 1: (s_guest'=1);
	[g1] (s_guest=1) & (is_g1_selected=true) -> 1: (s_guest'=1);
	[g2] (s_guest=1) & (is_g2_selected=true) -> 1: (s_guest'=1);
	[g3] (s_guest=1) & (is_g3_selected=true) -> 1: (s_guest'=1);
	[o1] (s_guest=1) & (is_o1_selected=true) -> 1: (s_guest'=1);
	[o2] (s_guest=1) & (is_o2_selected=true) -> 1: (s_guest'=1);
	[o3] (s_guest=1) & (is_o3_selected=true) -> 1: (s_guest'=1);
	
	[h1] (s_guest=2) & (is_h1_selected=true) -> 1: (s_guest'=2);
	[h2] (s_guest=2) & (is_h2_selected=true) -> 1: (s_guest'=2);
	[h3] (s_guest=2) & (is_h3_selected=true) -> 1: (s_guest'=2);
	[g1] (s_guest=2) & (is_g1_selected=true) -> 1: (s_guest'=2);
	[g2] (s_guest=2) & (is_g2_selected=true) -> 1: (s_guest'=2);
	[g3] (s_guest=2) & (is_g3_selected=true) -> 1: (s_guest'=2);
	[o1] (s_guest=2) & (is_o1_selected=true) -> 1: (s_guest'=2);
	[o2] (s_guest=2) & (is_o2_selected=true) -> 1: (s_guest'=2);
	[o3] (s_guest=2) & (is_o3_selected=true) -> 1: (s_guest'=2);
	
	[h1] (s_guest=3) & (is_h1_selected=true) -> 1: (s_guest'=3);
	[h2] (s_guest=3) & (is_h2_selected=true) -> 1: (s_guest'=3);
	[h3] (s_guest=3) & (is_h3_selected=true) -> 1: (s_guest'=3);
	[g1] (s_guest=3) & (is_g1_selected=true) -> 1: (s_guest'=3);
	[g2] (s_guest=3) & (is_g2_selected=true) -> 1: (s_guest'=3);
	[g3] (s_guest=3) & (is_g3_selected=true) -> 1: (s_guest'=3);
	[o1] (s_guest=3) & (is_o1_selected=true) -> 1: (s_guest'=3);
	[o2] (s_guest=3) & (is_o2_selected=true) -> 1: (s_guest'=3);
	[o3] (s_guest=3) & (is_o3_selected=true) -> 1: (s_guest'=3);
endmodule
