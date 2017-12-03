// create_file.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <fstream>
#include <windows.h>
#include <stdio.h>
#include <tchar.h>
#include <strsafe.h>

int main()
{
	if (true)
	{

	std::ofstream outfile0("firstfile.txt");
	outfile0 << "This is the first created file." << std::endl;
	outfile0.close();
	}
	else
	{
		// handle to a file
		HANDLE hFile;
		// file and path, change accordingly. LPCWSTR is a pointer to a constant
		// null-terminated string of 16-bit Unicode characters. It is a typedef:
		// typedef CONST WCHAR *LPCWSTR. The modifier 'L' is for wide character.
		LPCWSTR fname = L"secondfile.txt";
		DWORD lpdwFlags[100];
		BOOL test;

		char DataBuffer[] = "This is the second created file.";
		DWORD dwBytesToWrite = (DWORD)strlen(DataBuffer);
		DWORD dwBytesWritten = 0;
		BOOL bErrorFlag = FALSE;

		// Create a file with the given information...
		hFile = CreateFile(fname, // file to be opened
			GENERIC_WRITE, // open for writing
			FILE_SHARE_WRITE, // share for writing
			NULL, // default security
			CREATE_ALWAYS, // create new file only
			FILE_ATTRIBUTE_NORMAL | FILE_ATTRIBUTE_ARCHIVE | SECURITY_IMPERSONATION,
			// normal file archive and impersonate client
			NULL); // no attr. template

		if (hFile == INVALID_HANDLE_VALUE)
			printf("Could not open %s file, error %d\n", fname, GetLastError());
		else
		{
			printf("File's HANDLE is OK!\n");
			test = GetHandleInformation(hFile, lpdwFlags);
			printf("The return value is %d, error %d\n", test, GetLastError());
		}
		bErrorFlag = WriteFile(
			hFile,           // open file handle
			DataBuffer,      // start of data to write
			dwBytesToWrite,  // number of bytes to write
			&dwBytesWritten, // number of bytes that were written
			NULL);            // no overlapped structure

		if (FALSE == bErrorFlag)
		{
			printf("Terminal failure: Unable to write to file.\n");
		}
		else
		{
			if (dwBytesWritten != dwBytesToWrite)
			{
				// This is an error because a synchronous write that results in
				// success (WriteFile returns TRUE) should write all data as
				// requested. This would not necessarily be the case for
				// asynchronous writes.
				printf("Error: dwBytesWritten != dwBytesToWrite\n");
			}
			else
			{
				_tprintf(TEXT("Wrote %d bytes to %s successfully.\n"), dwBytesWritten, fname);
			}
		}
		// when finished, close the file handle
		CloseHandle(hFile);
		//DeleteFile(fname);
		return 0;
	}
}

