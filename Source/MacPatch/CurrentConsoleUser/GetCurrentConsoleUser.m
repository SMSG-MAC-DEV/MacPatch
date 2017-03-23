/*
 Copyright (c) 2017, Lawrence Livermore National Security, LLC.
 Produced at the Lawrence Livermore National Laboratory (cf, DISCLAIMER).
 Written by Charles Heizer <heizer1 at llnl.gov>.
 LLNL-CODE-636469 All rights reserved.
 
 This file is part of MacPatch, a program for installing and patching
 software.
 
 MacPatch is free software; you can redistribute it and/or modify it under
 the terms of the GNU General Public License (as published by the Free
 Software Foundation) version 2, dated June 1991.
 
 MacPatch is distributed in the hope that it will be useful, but WITHOUT ANY
 WARRANTY; without even the IMPLIED WARRANTY OF MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE. See the terms and conditions of the GNU General Public
 License for more details.
 
 You should have received a copy of the GNU General Public License along
 with MacPatch; if not, write to the Free Software Foundation, Inc.,
 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 */

#import <Foundation/Foundation.h>
#include <CoreFoundation/CoreFoundation.h>
#include <SystemConfiguration/SystemConfiguration.h>

int main (int argc, char * argv[])
{
    @autoreleasepool
    {
	
		int c;	
		while ((c = getopt (argc, argv, "v")) != -1)
			switch (c)
		{
			case 'v':
				fprintf (stdout, "1.1.0\n");
				return 0;
		}
		
		
		SCDynamicStoreRef   store;
		CFStringRef         consoleUserName;

		store = SCDynamicStoreCreate(NULL, (CFStringRef)@"GetCurrentConsoleUser", NULL, NULL);
		consoleUserName = SCDynamicStoreCopyConsoleUser(store, NULL, NULL);
		
		NSString *nsString = (__bridge NSString*)consoleUserName;
		if (nsString) {
			printf ("%s\n", [nsString UTF8String]);
		} else {
			printf ("null\n");
		}
        if (consoleUserName)
            CFRelease(consoleUserName);
	}
    return 0;
}