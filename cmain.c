#include <stdio.h>

void testcase_(int*i);
void shapeof_(void);

extern float* __mod_fu_MOD_uflux;
main(){
	printf("Hello world\n");
	
	int i=2;
	testcase_(&i);
	
	printf("__mod_fu_MOD_uflux[0] %f\n", __mod_fu_MOD_uflux[0]);
	printf("__mod_fu_MOD_uflux[0] %f\n", __mod_fu_MOD_uflux[1]);
	printf("__mod_fu_MOD_uflux[0] %f\n", __mod_fu_MOD_uflux[2]);
	
	shapeof_();
	
}