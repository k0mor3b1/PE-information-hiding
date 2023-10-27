#define BUILD_TEST
#include "test.h"
#include "stdio.h"
#include "pch.h"
#include <stdio.h>
#include<stdlib.h>

#define DLLEXPORT extern "C" __declspec(dllexport)    //直接在源文件定义导出


DLLEXPORT char* duan_name(char* filename)
{
	static char name[100] = { 0 };
	char a[2] = { 0 };
	a[0] = '@';
	HANDLE hfile = CreateFileA(
		filename,
		GENERIC_READ,
		FILE_SHARE_READ,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		0);
	if (hfile == INVALID_HANDLE_VALUE)
		printf("%d\n%s",GetLastError(),filename);
	DWORD fileSize = GetFileSize(hfile, NULL);
	char* fileBuff;
	fileBuff = (char*)malloc((size_t)fileSize);
	BOOL flag = FALSE;
	flag = ReadFile(hfile, fileBuff, fileSize, NULL, NULL);
	if (!flag)
		return name;
	PIMAGE_DOS_HEADER pDosHeaders = (PIMAGE_DOS_HEADER)fileBuff;
	PIMAGE_NT_HEADERS32 NTHead = (PIMAGE_NT_HEADERS32)(fileBuff + pDosHeaders->e_lfanew);
	PIMAGE_FILE_HEADER PEHead = &NTHead->FileHeader;
	PIMAGE_SECTION_HEADER PEZone = IMAGE_FIRST_SECTION(NTHead);
	for (int i = 0; i < PEHead->NumberOfSections; i++) {
		char b[9] = { 0 };
		int c = PEZone->SizeOfRawData - PEZone->Misc.VirtualSize;
		if (c < 0 )
		{
			c = 0;
		}
		char d[10] = { 0 };
		int radix = 10;
		itoa(c, d, radix);
		memcpy_s(b, 9, PEZone->Name, 8);
		strcat(name, b);
		strcat(name, a);
		strcat(name, d);
		strcat(name, a);
		PEZone++;
	}
	CloseHandle(hfile);
	return name;
}

/*初始化函数*/
void rc4_init(unsigned char* s, unsigned char* key, unsigned long Len)
{
	int i = 0, j = 0;
	char k[256] = { 0 };
	unsigned char tmp = 0;
	for (i = 0; i < 256; i++)
	{
		s[i] = i;
		k[i] = key[i % Len];
	}
	for (i = 0; i < 256; i++)
	{
		j = (j + s[i] + k[i]) % 256;
		tmp = s[i];
		s[i] = s[j];//交换s[i]和s[j]
		s[j] = tmp ^ 0x37;
	}
}

/*加解密*/
void rc4_crypt(unsigned char* s, unsigned char* Data, unsigned long Len)
{
	int i = 0, j = 0, t = 0;
	unsigned long k = 0;
	unsigned char tmp;
	for (k = 0; k < Len; k++)
	{
		i = (i + 1) % 256;
		j = (j + s[i]) % 256;
		tmp = s[i];
		s[i] = s[j];//交换s[x]和s[y]
		s[j] = tmp;
		t = (s[i] + s[j]) % 256;
		Data[k] ^= s[t];
	}
}

DLLEXPORT void jiami(char* Pwd, char* Ptext, char* filename, int duansum)
{
	char Password[7] = { 0 };
	char Plaintext[1000] = { 0 };
	unsigned char s[256] = { 0 };
	char key[7] = { "hxylss" };

	strcat(Password, Pwd);
	strcat(Plaintext, Ptext);

	rc4_init(s, (unsigned char*)key, strlen(key));//初始化
	rc4_crypt(s, (unsigned char*)Password, strlen(Password));//加密

	rc4_init(s, (unsigned char*)key, strlen(key));//初始化
	rc4_crypt(s, (unsigned char*)Plaintext, strlen(Plaintext));//加密

	HANDLE hfile = CreateFileA(
		filename,
		GENERIC_READ | GENERIC_WRITE,
		FILE_SHARE_READ,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		0);
	DWORD fileSize = GetFileSize(hfile, NULL);
	char* fileBuff;
	fileBuff = (char*)malloc((size_t)fileSize);
	BOOL flag = FALSE;
	flag = ReadFile(hfile, fileBuff, fileSize, NULL, NULL);

	DWORD yincang_pwd = SetFilePointer(hfile, 0, NULL, FILE_END);
	DWORD yin_pwd = 0;
	BOOL yin_p = WriteFile(hfile, Password, strlen(Password), &yin_pwd, NULL);

	PIMAGE_DOS_HEADER pDosHeaders = (PIMAGE_DOS_HEADER)fileBuff;//PE DOS头
	PIMAGE_NT_HEADERS32 NTHead = (PIMAGE_NT_HEADERS32)(fileBuff + pDosHeaders->e_lfanew);//PE NT头
	PIMAGE_FILE_HEADER PEHead = &NTHead->FileHeader;//PE头 
	PIMAGE_OPTIONAL_HEADER32 PEOptionalHeader = &NTHead->OptionalHeader;//PE可选头 
	PIMAGE_SECTION_HEADER PEZone = IMAGE_FIRST_SECTION(NTHead);//PE 节表头 

	for (int i = 0; i < duansum - 1; i++) {
		PEZone++;
	}

	DWORD yincang_data = SetFilePointer(hfile, PEZone->PointerToRawData + PEZone->SizeOfRawData - (PEZone->SizeOfRawData - PEZone->Misc.VirtualSize), NULL, 0);
	DWORD yinD = 0;
	BOOL yin = WriteFile(hfile, Plaintext, strlen(Plaintext), &yinD, NULL);

	DWORD yi;
	if (PEHead->SizeOfOptionalHeader == 0xE0)
		yi = 0x8;
	else
		yi = 0x18;
	DWORD pianyi = SetFilePointer(hfile, (pDosHeaders->e_lfanew + sizeof(IMAGE_NT_HEADERS32) + sizeof(IMAGE_SECTION_HEADER) * (duansum - 1) + yi), NULL, 0);
	DWORD VirtualSize = (DWORD)(PEZone->Misc.VirtualSize + (DWORD)strlen(Plaintext));
	DWORD dwWrited = 0;
	BOOL Write = WriteFile(hfile, &VirtualSize, sizeof(PEZone->Misc.VirtualSize), &dwWrited, NULL);
	
	CloseHandle(hfile);
}

DLLEXPORT char* jiemi(char* filename)
{
	static char mima[7] = { 0 };
	HANDLE hfile = CreateFileA(
		filename,
		GENERIC_READ,
		FILE_SHARE_READ,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		0);
	DWORD fileSize = GetFileSize(hfile, NULL);
	DWORD du_data = SetFilePointer(hfile, fileSize - 6, NULL, FILE_BEGIN);
	BOOL flag = FALSE;
	flag = ReadFile(hfile, mima, 6, NULL, NULL);
	CloseHandle(hfile);
	
	unsigned char s[256] = { 0 };
	char key[7] = { "hxylss" };

	rc4_init(s, (unsigned char*)key, strlen(key));//初始化
	rc4_crypt(s, (unsigned char*)mima, strlen(mima));//解密

	return mima;
}

DLLEXPORT void tiqu(char* filename, int duansum, int size)
{
	HANDLE hfile = CreateFileA(
		filename,
		GENERIC_READ,
		FILE_SHARE_READ,
		NULL,
		OPEN_EXISTING,
		FILE_ATTRIBUTE_NORMAL,
		0);
	DWORD fileSize = GetFileSize(hfile, NULL);
	char* fileBuff;
	fileBuff = (char*)malloc((size_t)fileSize);
	BOOL flag = FALSE;
	flag = ReadFile(hfile, fileBuff, fileSize, NULL, NULL);
	PIMAGE_DOS_HEADER pDosHeaders = (PIMAGE_DOS_HEADER)fileBuff;//PE DOS头
	PIMAGE_NT_HEADERS32 NTHead = (PIMAGE_NT_HEADERS32)(fileBuff + pDosHeaders->e_lfanew);//PE NT头
	PIMAGE_FILE_HEADER PEHead = &NTHead->FileHeader;//PE头 
	PIMAGE_OPTIONAL_HEADER32 PEOptionalHeader = &NTHead->OptionalHeader;//PE可选头 
	PIMAGE_SECTION_HEADER PEZone = IMAGE_FIRST_SECTION(NTHead);//PE 节表头 

	for (int i = 0; i < duansum - 1; i++) {
		PEZone++;
	}

	HANDLE Tfile = CreateFileA(
		"G:\\desktop\\123.txt",//文件路径 
		GENERIC_ALL,
		FILE_SHARE_READ,
		NULL,
		OPEN_ALWAYS,
		FILE_ATTRIBUTE_NORMAL,
		0);

	char* TfileBuff;
	TfileBuff = (char*)malloc(sizeof(char) * size);
	BOOL Tflag = FALSE;
	DWORD tiqu_data = SetFilePointer(hfile, PEZone->PointerToRawData + PEZone->Misc.VirtualSize - size, NULL, 0);

	Tflag = ReadFile(hfile, TfileBuff, size, NULL, NULL);
	
	char TFBuff[1000] = { 0 };
	unsigned char s[256] = { 0 };
	char key[7] = { "hxylss" };

	strcat(TFBuff, TfileBuff);
	rc4_init(s, (unsigned char*)key, strlen(key));//初始化
	rc4_crypt(s, (unsigned char*)TFBuff, strlen(TFBuff));//解密

	DWORD dwWrited = 0;
	BOOL Write = WriteFile(Tfile, TFBuff, size, &dwWrited, NULL);
	
	CloseHandle(Tfile);
	CloseHandle(hfile);
}
