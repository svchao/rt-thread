import os
# toolchains options
ARCH     = 'arm'
CPU      = 'arm926'
# toolchains options
CROSS_TOOL 	= 'gcc'

#------- toolchains path -------------------------------------------------------
if os.getenv('RTT_CC'):
	CROSS_TOOL = os.getenv('RTT_CC')

if  CROSS_TOOL == 'gcc':
	PLATFORM = 'gcc'
	EXEC_PATH = r'C:\Program Files (x86)\GNU Tools ARM Embedded\6 2017-q1-update\bin'
elif CROSS_TOOL == 'keil':
	PLATFORM 	= 'armcc'
	EXEC_PATH 	= r'C:\Keil_v5'

if os.getenv('RTT_EXEC_PATH'):
	EXEC_PATH = os.getenv('RTT_EXEC_PATH')

BUILD = 'debug'
#BUILD = 'release'

CORE = 'arm926ej-s'
MAP_FILE = 'rtthread_n9h30.map'
LINK_FILE = 'linking_scripts/n9h30'
TARGET_NAME = 'rtthread.bin'

#------- GCC settings ----------------------------------------------------------
if PLATFORM == 'gcc':
    # toolchains
    PREFIX = 'arm-none-eabi-'
    CC = PREFIX + 'gcc'
    CXX = PREFIX + 'g++'
    AS = PREFIX + 'gcc'
    AR = PREFIX + 'ar'
    LINK = PREFIX + 'gcc'
    TARGET_EXT = 'elf'
    SIZE = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY = PREFIX + 'objcopy'

    DEVICE = ' -mcpu=arm926ej-s'
    CFLAGS = DEVICE
    AFLAGS = '-c'+ DEVICE + ' -x assembler-with-cpp'
    AFLAGS += ' -Iplatform'
    LFLAGS = DEVICE
    LFLAGS += ' -Wl,--gc-sections,-cref,-Map=' + MAP_FILE
    LFLAGS += ' -T ' + LINK_FILE + '.ld'

    CPATH = ''
    LPATH = ''

    if BUILD == 'debug':
        CFLAGS += ' -O2 -gdwarf-2'
        AFLAGS += ' -gdwarf-2'
    else:
        CFLAGS += ' -O2'

    POST_ACTION = OBJCPY + ' -O binary $TARGET ' + TARGET_NAME + '\n' 
    POST_ACTION += SIZE + ' $TARGET\n'
#------- Keil settings ---------------------------------------------------------
elif PLATFORM == 'armcc':
    # toolchains
    CC = 'armcc'
    AS = 'armasm'
    AR = 'armar'
    LINK = 'armlink'
    TARGET_EXT = 'axf'
    EXEC_PATH += '/arm/armcc/bin/'

    DEVICE = ' --cpu=' + CORE
    CFLAGS = DEVICE + ' --apcs=interwork --diag_suppress=870'
    AFLAGS = DEVICE + ' -Iplatform'
    LFLAGS = DEVICE + ' --strict'
    LFLAGS += ' --info sizes --info totals --info unused --info veneers'
    LFLAGS += ' --list ' + MAP_FILE
    LFLAGS += ' --scatter  ' + LINK_FILE + '.sct'

    if BUILD == 'debug':
        CFLAGS += ' -g -O0'
        AFLAGS += ' -g'
    else:
        CFLAGS += ' -O2'

    POST_ACTION = 'fromelf --bin $TARGET --output ' + TARGET_NAME + ' \n'
    POST_ACTION += 'fromelf -z $TARGET\n'