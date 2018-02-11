// registry_example.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "windows.h"
#include <iostream>

using namespace std;

HKEY OpenKey(HKEY hRootKey, wchar_t* strKey)
{
	HKEY hKey;
	LONG nError = RegOpenKeyEx(hRootKey, strKey, NULL, KEY_ALL_ACCESS, &hKey);

	if (nError == ERROR_FILE_NOT_FOUND)
	{
		//cout << "Creating registry key: " << strKey << endl;
		nError = RegCreateKeyEx(hRootKey, strKey, NULL, NULL, REG_OPTION_NON_VOLATILE, KEY_ALL_ACCESS, NULL, &hKey, NULL);
	}

	if (nError)
		cout << "Error: " << nError << " Could not find or create " << strKey << endl;

	return hKey;
}

void SetValBinary(HKEY hKey, LPCTSTR lpValue, char data[15], int size)
{
	LONG nError = RegSetValueEx(hKey, lpValue, NULL, REG_BINARY, (LPBYTE)data, size);

	if (nError)
		cout << "Error: " << nError << " Could not set registry value: " << (char*)lpValue << endl;
}

void SetValDWORD(HKEY hKey, LPCTSTR lpValue, DWORD data)
{
	
	LONG nError = RegSetValueEx(hKey, lpValue, NULL, REG_DWORD, (const BYTE*)&data, sizeof(data));

	if (nError)
		cout << "Error: " << nError << " Could not set registry value: " << (char*)lpValue << endl;
}


void SetValStrings(HKEY hKey, LPCTSTR lpValue, std::wstring data)
{
	int size1 = data.size();
	printf("%d",size1);
	// Due to the data size is base on two digits in Byte, data.size() * 2 is required instead of data.size() + 1
	LONG nError = RegSetValueEx(hKey, lpValue, NULL, REG_SZ, (LPBYTE)(data.c_str()), data.size() * 2);

	if (nError)
		cout << "Error: " << nError << " Could not set registry value: " << (char*)lpValue << endl;
}

DWORD GetValBinary(HKEY hKey, LPCTSTR lpValue)
{
	DWORD data;		DWORD size = sizeof(data);	DWORD type = REG_BINARY;
	LONG nError = RegQueryValueEx(hKey, lpValue, NULL, &type, (LPBYTE)&data, &size);

	if (nError == ERROR_FILE_NOT_FOUND)
		data = 0; // The value will be created and set to data next time SetVal() is called.
	else if (nError)
		cout << "Error: " << nError << " Could not get registry value " << (char*)lpValue << endl;

	return data;
}

DWORD GetValData(HKEY hKey, LPCTSTR lpValue)
{
	DWORD data;		DWORD size = sizeof(data);	DWORD type = REG_DWORD;
	LONG nError = RegQueryValueEx(hKey, lpValue, NULL, &type, (LPBYTE)&data, &size);

	if (nError == ERROR_FILE_NOT_FOUND)
		data = 0; // The value will be created and set to data next time SetVal() is called.
	else if (nError)
		cout << "Error: " << nError << " Could not get registry value " << (char*)lpValue << endl;

	return data;
}

int main()
{
	//*** New Registry Creation ***//

	// setting up new key //
	// List of HKEY:
	// HKEY_LOCAL_MACHINE HKLM
	// HKEY_CURRENT_CONFIG HKCC
	// HKEY_CLASSES_ROOT HKCR
	// HKEY_CURRENT_USER HKCU
	// HKEY_USERS HKU
	// OpenKey(HKEY, LongWord"registry_key\\registry_key_path2\\path3\\");
	
	HKEY hKey = OpenKey(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\CLSUID");

	// Write new resgitry key value //
	// Write in HEX value for binary
	
	// Declare char array, size of array needs to be same as the binary
	char exe[14] = { 0x54,0x68,0x69,0x73,0x20,0x69,0x73,0x20,0x61,0x20,0x74,0x65,0x73,0x74 };
	//0x54 0x68 0x69 0x73 0x20 0x69 0x73 0x20 0x61 0x20 0x74 0x65 0x73 0x74
	// Calculate the size of the array
	int size_exe = sizeof(exe);
	// Add the resgitry key value
	SetValBinary(hKey, L"Binary_Value", exe, size_exe);

	// Write new resgitry key value //
	// Write in value for DWORD

	static DWORD dwords;
	dwords = 1;

	SetValDWORD(hKey, L"Dword_Value", dwords);
	
	std::wstring a = TEXT("DWORD often use as indicate 0 and 1.");
	//printf("%s",a);
	SetValStrings(hKey, L"String_Value", a);

	// Close registry key //
	RegCloseKey(hKey);

	//*** End of Registry Key Creation ***//

    return 0;
}

