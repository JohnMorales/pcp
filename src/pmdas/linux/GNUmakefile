#
# Copyright (c) 2000,2003,2004,2008 Silicon Graphics, Inc.  All Rights Reserved.
# Copyright (c) 2007-2010 Aconex.  All Rights Reserved.
# Copyright (c) 2013-2015 Red Hat.
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
#

TOPDIR = ../../..
include	$(TOPDIR)/src/include/builddefs

IAM		= linux
DOMAIN		= LINUX
CMDTARGET	= pmdalinux
LIBTARGET	= pmda_linux.so
PMDAINIT	= linux_init
PMDADIR		= $(PCP_PMDAS_DIR)/$(IAM)
LOGREWRITEDIR	= $(PCP_VAR_DIR)/config/pmlogrewrite
CONF_LINE	= "linux	60	pipe	binary		$(PMDADIR)/$(CMDTARGET)"

CFILES		= pmda.c \
		  proc_stat.c proc_meminfo.c proc_loadavg.c \
		  proc_net_dev.c interrupts.c filesys.c \
		  swapdev.c devmapper.c proc_net_rpc.c proc_partitions.c \
		  getinfo.c proc_net_sockstat.c proc_net_snmp.c \
		  proc_scsi.c proc_cpuinfo.c proc_net_tcp.c \
		  proc_slabinfo.c sem_limits.c msg_limits.c shm_limits.c \
		  proc_uptime.c proc_sys_fs.c proc_vmstat.c \
		  sysfs_kernel.c linux_table.c numa_meminfo.c \
		  proc_net_netstat.c namespaces.c

HFILES		= clusters.h indom.h convert.h \
		  proc_stat.h proc_meminfo.h proc_loadavg.h \
		  proc_net_dev.h interrupts.h filesys.h \
		  swapdev.h devmapper.h proc_net_rpc.h proc_partitions.h \
		  getinfo.h proc_net_sockstat.h proc_net_snmp.h \
		  proc_scsi.h proc_cpuinfo.h proc_net_tcp.h \
		  proc_slabinfo.h sem_limits.h msg_limits.h shm_limits.h \
		  proc_uptime.h proc_sys_fs.h proc_vmstat.h \
		  sysfs_kernel.h linux_table.h numa_meminfo.h \
		  proc_net_netstat.h namespaces.h

VERSION_SCRIPT	= exports
HELPTARGETS	= help.dir help.pag
LSRCFILES 	= help root_linux proc_net_snmp_migrate.conf
LDIRT		= $(HELPTARGETS) domain.h $(VERSION_SCRIPT)

LLDLIBS		= $(PCP_PMDALIB)
LCFLAGS		= $(INVISIBILITY)

# Uncomment these flags for profiling
# LCFLAGS	+= -pg
# LLDFLAGS	+= -pg

default:	build-me

include $(BUILDRULES)

ifeq "$(TARGET_OS)" "linux"
build-me: domain.h $(LIBTARGET) $(CMDTARGET) $(HELPTARGETS)
	@if [ -f ../pmcd.conf ]; then \
	    if [ `grep -c $(CONF_LINE) ../pmcd.conf` -eq 0 ]; then \
		echo $(CONF_LINE) >> ../pmcd.conf ; \
	    fi; \
	fi

install: default
	$(INSTALL) -m 755 -d $(PMDADIR)
	$(INSTALL) -m 644 domain.h help $(HELPTARGETS) $(PMDADIR)
	$(INSTALL) -m 755 $(LIBTARGET) $(CMDTARGET) $(PMDADIR)
	$(INSTALL) -m 644 root_linux $(PCP_VAR_DIR)/pmns/root_linux
	$(INSTALL) -m 644 proc_net_snmp_migrate.conf $(LOGREWRITEDIR)/linux_proc_net_snmp_migrate.conf
else
build-me:
install:
endif

default_pcp : default

install_pcp : install

$(HELPTARGETS) : help
	$(RUN_IN_BUILD_ENV) $(TOPDIR)/src/newhelp/newhelp -n root_linux -v 2 -o help < help

$(VERSION_SCRIPT):
	$(VERSION_SCRIPT_MAKERULE)

domain.h: ../../pmns/stdpmid
	$(DOMAIN_MAKERULE)

interrupts.o pmda.o proc_partitions.o:	clusters.h
pmda.o proc_partitions.o:	convert.h
pmda.o:	domain.h
filesys.o interrupts.o pmda.o:	filesys.h
pmda.o:	getinfo.h
pmda.o devmapper.o:	devmapper.h
numa_meminfo.o pmda.o proc_cpuinfo.o proc_partitions.o proc_stat.o:	indom.h
interrupts.o pmda.o:	interrupts.h
linux_table.o numa_meminfo.o pmda.o:	linux_table.h
msg_limits.o pmda.o:	msg_limits.h
numa_meminfo.o pmda.o:	numa_meminfo.h
pmda.o proc_cpuinfo.o proc_stat.o:	proc_cpuinfo.h
pmda.o proc_loadavg.o:	proc_loadavg.h
pmda.o proc_meminfo.o:	proc_meminfo.h
pmda.o proc_net_dev.o:	proc_net_dev.h
pmda.o proc_net_netstat.o:	proc_net_netstat.h
pmda.o proc_net_rpc.o:	proc_net_rpc.h
pmda.o proc_net_snmp.o:	proc_net_snmp.h
pmda.o proc_net_sockstat.o:	proc_net_sockstat.h
pmda.o proc_net_tcp.o:	proc_net_tcp.h
pmda.o proc_partitions.o:	proc_partitions.h
pmda.o proc_scsi.o:	proc_scsi.h
pmda.o proc_slabinfo.o:	proc_slabinfo.h
pmda.o proc_stat.o:	proc_stat.h
pmda.o proc_sys_fs.o:	proc_sys_fs.h
pmda.o proc_uptime.o:	proc_uptime.h
pmda.o proc_vmstat.o:	proc_vmstat.h
pmda.o sem_limits.o:	sem_limits.h
pmda.o shm_limits.o:	shm_limits.h
pmda.o swapdev.o:	swapdev.h
pmda.o sysfs_kernel.o:	sysfs_kernel.h
pmda.o:	$(VERSION_SCRIPT)
