#pragma once

#ifdef BUILD_TEST
#define API_SYMBOL __declspec(dllexport)	//导出函数
#else
#define API_SYMBOL __declspec(dllimport)	//导入函数
#endif
//宏定义，导出或者导入//
//PE
extern "C" API_SYMBOL char* duan_name(char *filename);
extern "C" API_SYMBOL void jiami(char* Password, char* Plaintext, char* filename, int duansum);
extern "C" API_SYMBOL char* jiemi(char* filename);
extern "C" API_SYMBOL void tiqu(char* filename, int duansum, int size);
extern "C" API_SYMBOL void rc4_init(unsigned char* s, unsigned char* key, unsigned long Len);
extern "C" API_SYMBOL void rc4_crypt(unsigned char* s, unsigned char* Data, unsigned long Len);
//导出函数//#pragma once
