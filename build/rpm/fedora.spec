Summary: System-level performance monitoring and performance management
Name: pcp
Version: 3.10.4
%global buildversion 1

Release: %{buildversion}%{?dist}
License: GPLv2+ and LGPLv2.1+ and CC-BY
URL: http://www.pcp.io
Group: Applications/System
Source0: ftp://ftp.pcp.io/projects/pcp/download/%{name}-%{version}.src.tar.gz
# From: git://sourceware.org/git/pcpfans.git --branch=webjs
Source1: pcp-webjs.src.tar.gz

# There are no papi/libpfm devel packages for s390 nor for some rhels, disable
%ifarch s390 s390x
%global disable_papi 1
%global disable_perfevent 1
%else
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
%global disable_papi 0
%else
%global disable_papi 1
%endif
%if 0%{?fedora} >= 20 || 0%{?rhel} > 6
%global disable_perfevent 0
%else
%global disable_perfevent 1
%endif
%endif

%global disable_microhttpd 0
%global disable_cairo 0

%global disable_python2 0
# Default for epel5 is python24, so use the (optional) python26 packages
%if 0%{?rhel} == 5
%global default_python 26
%endif
# No python3 development environment before el7
%if 0%{?rhel} == 0 || 0%{?rhel} > 6
%global disable_python3 0
# Do we wish to mandate python3 use in pcp?  (f22+ and el8+)
%if 0%{?fedora} >= 22 || 0%{?rhel} >= 8
%global default_python 3
%endif
%else
%global disable_python3 1
%endif

# Qt development and runtime environment missing components before el6
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
%global disable_qt 0
%else
%global disable_qt 1
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: procps autoconf bison flex
BuildRequires: nss-devel
BuildRequires: rpm-devel
BuildRequires: avahi-devel
%if !%{disable_python2}
%if 0%{?default_python} != 3
BuildRequires: python%{?default_python}-devel
%else
BuildRequires: python-devel
%endif
%endif
%if !%{disable_python3}
BuildRequires: python3-devel
%endif
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: cyrus-sasl-devel
%if !%{disable_papi}
BuildRequires: papi-devel
%endif
%if !%{disable_perfevent}
BuildRequires: libpfm-devel >= 4
%endif
%if !%{disable_microhttpd}
BuildRequires: libmicrohttpd-devel
%endif
%if !%{disable_cairo}
BuildRequires: cairo-devel
%endif
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
BuildRequires: systemtap-sdt-devel
%else
%ifnarch ppc ppc64
BuildRequires: systemtap-sdt-devel
%endif
%endif
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: initscripts man
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 7
BuildRequires: systemd-devel
%endif
%if !%{disable_qt}
BuildRequires: desktop-file-utils
BuildRequires: qt4-devel >= 4.4
%endif

Requires: bash gawk sed grep fileutils findutils initscripts perl which
Requires: python%{?default_python}
Requires: pcp-libs = %{version}-%{release}
%if 0%{?default_python} == 3
Requires: python3-pcp = %{version}-%{release}
%endif
%if !%{disable_python2} && 0%{?default_python} != 3
Requires: python-pcp = %{version}-%{release}
%endif
Requires: perl-PCP-PMDA = %{version}-%{release}
Obsoletes: pcp-gui-debuginfo
Obsoletes: pcp-pmda-nvidia

%global tapsetdir      %{_datadir}/systemtap/tapset

%global _confdir  %{_sysconfdir}/pcp
%global _logsdir  %{_localstatedir}/log/pcp
%global _pmnsdir  %{_localstatedir}/lib/pcp/pmns
%global _tempsdir %{_localstatedir}/lib/pcp/tmp
%global _pmdasdir %{_localstatedir}/lib/pcp/pmdas
%global _testsdir %{_localstatedir}/lib/pcp/testsuite
%global _pixmapdir %{_datadir}/pcp-gui/pixmaps
%global _booksdir %{_datadir}/doc/pcp-doc

%if 0%{?fedora} >= 20 || 0%{?rhel} >= 8
%global _with_doc --with-docdir=%{_docdir}/%{name}
%endif
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%global _initddir %{_datadir}/pcp/lib
%global disable_systemd 0
%else
%global _initddir %{_sysconfdir}/rc.d/init.d
%global _with_initd --with-rcdir=%{_initddir}
%global disable_systemd 1
%endif

# we never want Infiniband on s390 platforms
%ifarch s390 s390x
%global disable_infiniband 1
%else
# we never want Infiniband on RHEL5 or earlier
%if 0%{?rhel} != 0 && 0%{?rhel} < 6
%global disable_infiniband 1
%else
%global disable_infiniband 0
%endif
%endif

%if %{disable_infiniband}
%global _with_ib --with-infiniband=no
%endif

%if !%{disable_papi}
%global _with_papi --with-papi=yes
%endif

%if !%{disable_perfevent}
%global _with_perfevent --with-perfevent=yes
%endif


%description
Performance Co-Pilot (PCP) provides a framework and services to support
system-level performance monitoring and performance management. 

The PCP open source release provides a unifying abstraction for all of
the interesting performance data in a system, and allows client
applications to easily retrieve and process any subset of that data. 

#
# pcp-conf
#
%package conf
License: LGPLv2+
Group: System Environment/Libraries
Summary: Performance Co-Pilot run-time configuration
URL: http://www.pcp.io

# http://fedoraproject.org/wiki/Packaging:Conflicts "Splitting Packages"
Conflicts: pcp-libs < 3.9

%description conf
Performance Co-Pilot (PCP) run-time configuration

#
# pcp-libs
#
%package libs
License: LGPLv2+
Group: System Environment/Libraries
Summary: Performance Co-Pilot run-time libraries
URL: http://www.pcp.io
Requires: pcp-conf = %{version}-%{release}

%description libs
Performance Co-Pilot (PCP) run-time libraries

#
# pcp-libs-devel
#
%package libs-devel
License: GPLv2+ and LGPLv2.1+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) development headers and documentation
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release}
Requires: pcp-libs = %{version}-%{release}

%description libs-devel
Performance Co-Pilot (PCP) headers, documentation and tools for development.

#
# pcp-testsuite
#
%package testsuite
License: GPLv2+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) test suite
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release}
Requires: pcp-libs = %{version}-%{release}
Requires: pcp-libs-devel = %{version}-%{release}
Obsoletes: pcp-gui-testsuite

%description testsuite
Quality assurance test suite for Performance Co-Pilot (PCP).

#
# pcp-manager
#
%package manager
License: GPLv2+
Group: Applications/System
Summary: Performance Co-Pilot (PCP) manager daemon
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description manager
An optional daemon (pmmgr) that manages a collection of pmlogger and
pmie daemons, for a set of discovered local and remote hosts running
the performance metrics collection daemon (pmcd).  It ensures these
daemons are running when appropriate, and manages their log rotation
needs.  It is an alternative to the cron-based pmlogger/pmie service
scripts.

%if !%{disable_microhttpd}
#
# pcp-webapi
#
%package webapi
License: GPLv2+
Group: Applications/System
Summary: Performance Co-Pilot (PCP) web API service
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description webapi
Provides a daemon (pmwebd) that binds a large subset of the Performance
Co-Pilot (PCP) client API (PMAPI) to RESTful web applications using the
HTTP (PMWEBAPI) protocol.
%endif

#
# pcp-webjs and pcp-webapp packages
#
%package webjs
License: ASL2.0 and MIT and CC-BY
Group: Applications/Internet
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
BuildArch: noarch
%endif
Requires: pcp-webapp-graphite pcp-webapp-grafana pcp-webapp-vector
Summary: Performance Co-Pilot (PCP) web applications
URL: http://www.pcp.io

%description webjs
Javascript web application content for the Performance Co-Pilot (PCP)
web service.

%package webapp-vector
License: ASL2.0
Group: Applications/Internet
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
BuildArch: noarch
%endif
Summary: Vector web application for Performance Co-Pilot (PCP)
URL: https://github.com/Netflix/vector

%description webapp-vector
Vector web application for the Performance Co-Pilot (PCP).

%package webapp-grafana
License: ASL2.0
Group: Applications/Internet
Conflicts: pcp-webjs < 3.10.4
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
BuildArch: noarch
%endif
Summary: Grafana web application for Performance Co-Pilot (PCP)
URL: https://grafana.org

%description webapp-grafana
Grafana is an open source, feature rich metrics dashboard and graph
editor.  This package provides a Grafana that uses the Performance
Co-Pilot (PCP) as the data repository.  Other Grafana backends are
not used.

Grafana can render time series dashboards at the browser via flot.js
(more interactive, slower, for beefy browsers) or alternately at the
server via png (less interactive, faster).

%package webapp-graphite
License: ASL2.0
Group: Applications/Internet
Conflicts: pcp-webjs < 3.10.4
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
BuildArch: noarch
%endif
Summary: Graphite web application for Performance Co-Pilot (PCP)
URL: http://graphite.readthedocs.org

%description webapp-graphite
Graphite is a highly scalable real-time graphing system. This package
provides a graphite version that uses the Performance Co-Pilot (PCP)
as the data repository, and Graphites web interface renders it. The
Carbon and Whisper subsystems of Graphite are not included nor used.

#
# perl-PCP-PMDA. This is the PCP agent perl binding.
#
%package -n perl-PCP-PMDA
License: GPLv2+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) Perl bindings and documentation
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}

%description -n perl-PCP-PMDA
The PCP::PMDA Perl module contains the language bindings for
building Performance Metric Domain Agents (PMDAs) using Perl.
Each PMDA exports performance data for one specific domain, for
example the operating system kernel, Cisco routers, a database,
an application, etc.

#
# perl-PCP-MMV
#
%package -n perl-PCP-MMV
License: GPLv2+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) Perl bindings for PCP Memory Mapped Values
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}

%description -n perl-PCP-MMV
The PCP::MMV module contains the Perl language bindings for
building scripts instrumented with the Performance Co-Pilot
(PCP) Memory Mapped Value (MMV) mechanism.
This mechanism allows arbitrary values to be exported from an
instrumented script into the PCP infrastructure for monitoring
and analysis with pmchart, pmie, pmlogger and other PCP tools.

#
# perl-PCP-LogImport
#
%package -n perl-PCP-LogImport
License: GPLv2+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) Perl bindings for importing external data into PCP archives
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}

%description -n perl-PCP-LogImport
The PCP::LogImport module contains the Perl language bindings for
importing data in various 3rd party formats into PCP archives so
they can be replayed with standard PCP monitoring tools.

#
# perl-PCP-LogSummary
#
%package -n perl-PCP-LogSummary
License: GPLv2+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) Perl bindings for post-processing output of pmlogsummary
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}

%description -n perl-PCP-LogSummary
The PCP::LogSummary module provides a Perl module for using the
statistical summary data produced by the Performance Co-Pilot
pmlogsummary utility.  This utility produces various averages,
minima, maxima, and other calculations based on the performance
data stored in a PCP archive.  The Perl interface is ideal for
exporting this data into third-party tools (e.g. spreadsheets).

#
# pcp-import-sar2pcp
#
%package import-sar2pcp
License: LGPLv2+
Group: Applications/System
Summary: Performance Co-Pilot tools for importing sar data into PCP archive logs
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}
Requires: sysstat

%description import-sar2pcp
Performance Co-Pilot (PCP) front-end tools for importing sar data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-iostat2pcp
#
%package import-iostat2pcp
License: LGPLv2+
Group: Applications/System
Summary: Performance Co-Pilot tools for importing iostat data into PCP archive logs
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}
Requires: sysstat

%description import-iostat2pcp
Performance Co-Pilot (PCP) front-end tools for importing iostat data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-mrtg2pcp
#
%package import-mrtg2pcp
License: LGPLv2+
Group: Applications/System
Summary: Performance Co-Pilot tools for importing MTRG data into PCP archive logs
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-mrtg2pcp
Performance Co-Pilot (PCP) front-end tools for importing MTRG data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-ganglia2pcp
#
%package import-ganglia2pcp
License: LGPLv2+
Group: Applications/System
Summary: Performance Co-Pilot tools for importing ganglia data into PCP archive logs
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}
Requires: perl-PCP-LogImport = %{version}-%{release}

%description import-ganglia2pcp
Performance Co-Pilot (PCP) front-end tools for importing ganglia data
into standard PCP archive logs for replay with any PCP monitoring tool.

#
# pcp-import-collectl2pcp
#
%package import-collectl2pcp
License: LGPLv2+
Group: Applications/System
Summary: Performance Co-Pilot tools for importing collectl log files into PCP archive logs
URL: http://www.pcp.io
Requires: pcp-libs = %{version}-%{release}

%description import-collectl2pcp
Performance Co-Pilot (PCP) front-end tools for importing collectl data
into standard PCP archive logs for replay with any PCP monitoring tool.

%if !%{disable_papi}
#
# pcp-pmda-papi
#
%package pmda-papi
License: GPLv2+
Group: Applications/System
Summary: Performance Co-Pilot (PCP) metrics for Performance API and hardware counters
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
BuildRequires: papi-devel

%description pmda-papi
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting hardware counters statistics through PAPI (Performance API).
%endif

%if !%{disable_perfevent}
#
# pcp-pmda-perfevent
#
%package pmda-perfevent
License: GPLv2+
Group: Applications/System
Summary: Performance Co-Pilot (PCP) metrics for hardware counters
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libpfm >= 4
BuildRequires: libpfm-devel >= 4

%description pmda-perfevent
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting hardware counters statistics through libpfm.
%endif

%if !%{disable_infiniband}
#
# pcp-pmda-infiniband
#
%package pmda-infiniband
License: GPLv2+
Group: Applications/System
Summary: Performance Co-Pilot (PCP) metrics for Infiniband HCAs and switches
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}
Requires: libibmad >= 1.3.7 libibumad >= 1.3.7
BuildRequires: libibmad-devel >= 1.3.7 libibumad-devel >= 1.3.7

%description pmda-infiniband
This package contains the PCP Performance Metrics Domain Agent (PMDA) for
collecting Infiniband statistics.  By default, it monitors the local HCAs
but can also be configured to monitor remote GUIDs such as IB switches.
%endif

%if !%{disable_python2}
#
# python-pcp. This is the PCP library bindings for python.
#
%package -n python-pcp
License: GPLv2+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) Python bindings and documentation
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description -n python-pcp
This python PCP module contains the language bindings for
Performance Metric API (PMAPI) monitor tools and Performance
Metric Domain Agent (PMDA) collector tools written in Python.
%endif

%if !%{disable_python3}
#
# python3-pcp. This is the PCP library bindings for python3.
#
%package -n python3-pcp
License: GPLv2+
Group: Development/Libraries
Summary: Performance Co-Pilot (PCP) Python3 bindings and documentation
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description -n python3-pcp
This python PCP module contains the language bindings for
Performance Metric API (PMAPI) monitor tools and Performance
Metric Domain Agent (PMDA) collector tools written in Python3.
%endif

%if !%{disable_qt}
#
# pcp-gui package for Qt tools
#
%package -n pcp-gui
License: GPLv2+ and LGPLv2+ and LGPLv2+ with exceptions
Group: Applications/System
Summary: Visualization tools for the Performance Co-Pilot toolkit
URL: http://www.pcp.io
Requires: pcp = %{version}-%{release} pcp-libs = %{version}-%{release}

%description -n pcp-gui
Visualization tools for the Performance Co-Pilot toolkit.
The pcp-gui package primarily includes visualization tools for
monitoring systems using live and archived Performance Co-Pilot
(PCP) sources.
%endif

#
# pcp-doc package
#
%package -n pcp-doc
License: GPLv2+ and CC-BY
Group: Documentation
%if 0%{?rhel} == 0 || 0%{?rhel} > 5
BuildArch: noarch
%endif
Summary: Documentation and tutorial for the Performance Co-Pilot
URL: http://www.pcp.io

%description -n pcp-doc
Documentation and tutorial for the Performance Co-Pilot
Performance Co-Pilot (PCP) provides a framework and services to support
system-level performance monitoring and performance management.

The pcp-doc package provides useful information on using and
configuring the Performance Co-Pilot (PCP) toolkit for system
level performance management.  It includes tutorials, HOWTOs,
and other detailed documentation about the internals of core
PCP utilities and daemons, and the PCP graphical tools.

%prep
%setup -q
%setup -q -T -D -a 1

%clean
rm -Rf $RPM_BUILD_ROOT

%build
%if !%{disable_python2} && 0%{?default_python} != 3
export PYTHON=python%{?default_python}
%endif
%configure %{?_with_initd} %{?_with_doc} %{?_with_ib} %{?_with_papi} %{?_with_perfevent}
make default_pcp

%install
rm -Rf $RPM_BUILD_ROOT
export NO_CHOWN=true DIST_ROOT=$RPM_BUILD_ROOT
make install_pcp

PCP_GUI='pmchart|pmconfirm|pmdumptext|pmmessage|pmquery|pmsnap|pmtime'

# Fix stuff we do/don't want to ship
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.a

# remove sheet2pcp until BZ 830923 and BZ 754678 are resolved.
rm -f $RPM_BUILD_ROOT/%{_bindir}/sheet2pcp $RPM_BUILD_ROOT/%{_mandir}/man1/sheet2pcp.1*

# remove configsz.h as this is not multilib friendly.
rm -f $RPM_BUILD_ROOT/%{_includedir}/pcp/configsz.h

%if %{disable_microhttpd}
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/pmwebd.*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man3/PMWEBAPI.*
rm -fr $RPM_BUILD_ROOT/%{_confdir}/pmwebd
rm -fr $RPM_BUILD_ROOT/%{_initddir}/pmwebd
rm -fr $RPM_BUILD_ROOT/%{_unitdir}/pmwebd.service
rm -f $RPM_BUILD_ROOT/%{_libexecdir}/pcp/bin/pmwebd
%endif
mv pcp-webjs/* $RPM_BUILD_ROOT/%{_datadir}/pcp/webapps
rmdir pcp-webjs

%if %{disable_infiniband}
# remove pmdainfiniband on platforms lacking IB devel packages.
rm -f $RPM_BUILD_ROOT/%{_pmdasdir}/ib
rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/pmdaib.1*
rm -fr $RPM_BUILD_ROOT/%{_pmdasdir}/infiniband
%endif

%if %{disable_qt}
rm -fr $RPM_BUILD_ROOT/%{_pixmapdir}
rm -fr $RPM_BUILD_ROOT/%{_confdir}/pmsnap
rm -fr $RPM_BUILD_ROOT/%{_localstatedir}/lib/pcp/config/pmsnap
rm -fr $RPM_BUILD_ROOT/%{_localstatedir}/lib/pcp/config/pmchart
rm -f $RPM_BUILD_ROOT/%{_localstatedir}/lib/pcp/config/pmafm/pcp-gui
rm -f $RPM_BUILD_ROOT/%{_datadir}/applications/pmchart.desktop
rm -f `find $RPM_BUILD_ROOT/%{_mandir}/man1 | grep -E "$PCP_GUI"`
%else
rm -rf $RPM_BUILD_ROOT/usr/share/doc/pcp-gui
desktop-file-validate $RPM_BUILD_ROOT/%{_datadir}/applications/pmchart.desktop
%endif

# default chkconfig off for Fedora and RHEL
for f in $RPM_BUILD_ROOT/%{_initddir}/{pcp,pmcd,pmlogger,pmie,pmwebd,pmmgr,pmproxy}; do
	test -f "$f" || continue
	sed -i -e '/^# chkconfig/s/:.*$/: - 95 05/' -e '/^# Default-Start:/s/:.*$/:/' $f
done

%if 0%{?default_python} != 0
# defaulting to explicit python version requires /usr/bin/pythonN hashbang
# lines (for either python3 or python26 on epel5), make it so:
for f in `find $RPM_BUILD_ROOT -type f -print`
do
    sed -i -e "1 s|^#!/usr/bin/python\b|#!/usr/bin/python%{default_python}|" $f
done
%endif

# list of PMDAs in the base pkg
ls -1 $RPM_BUILD_ROOT/%{_pmdasdir} |\
  grep -E -v 'simple|sample|trivial|txmon' |\
  grep -E -v 'perfevent|perfalloc.1' |\
  grep -E -v '^ib$|infiniband' |\
  grep -E -v 'papi' |\
  sed -e 's#^#'%{_pmdasdir}'\/#' >base_pmdas.list

# all base pcp package files except those split out into sub packages
ls -1 $RPM_BUILD_ROOT/%{_bindir} |\
  sed -e 's#^#'%{_bindir}'\/#' >base_bin.list
ls -1 $RPM_BUILD_ROOT/%{_libexecdir}/pcp/bin |\
  sed -e 's#^#'%{_libexecdir}/pcp/bin'\/#' >base_exec.list
ls -1 $RPM_BUILD_ROOT/%{_mandir}/man1 |\
  sed -e 's#^#'%{_mandir}'\/man1\/#' >base_man.list
ls -1 $RPM_BUILD_ROOT/%{_booksdir} |\
  sed -e 's#^#'%{_booksdir}'\/#' > pcp-doc.list
ls -1 $RPM_BUILD_ROOT/%{_datadir}/pcp/demos/tutorials |\
  sed -e 's#^#'%{_datadir}/pcp/demos/tutorials'\/#' >>pcp-doc.list
%if !%{disable_qt}
ls -1 $RPM_BUILD_ROOT/%{_pixmapdir} |\
  sed -e 's#^#'%{_pixmapdir}'\/#' > pcp-gui.list
cat base_bin.list base_exec.list base_man.list |\
  grep -E "$PCP_GUI" >> pcp-gui.list
%endif
cat base_pmdas.list base_bin.list base_exec.list base_man.list |\
  grep -E -v 'pmdaib|pmmgr|pmweb|pmsnap|2pcp' |\
  grep -E -v "$PCP_GUI|pixmaps|pcp-doc|tutorials" |\
  grep -E -v %{_confdir} | grep -E -v %{_logsdir} > base.list

# all devel pcp package files except those split out into sub packages
ls -1 $RPM_BUILD_ROOT/%{_mandir}/man3 |\
sed -e 's#^#'%{_mandir}'\/man3\/#' | grep -E -v '3pm|PMWEBAPI' >devel.list
ls -1 $RPM_BUILD_ROOT/%{_datadir}/pcp/demos |\
sed -e 's#^#'%{_datadir}'\/pcp\/demos\/#' | grep -E -v tutorials >> devel.list

%pre testsuite
test -d %{_testsdir} || mkdir -p -m 755 %{_testsdir}
getent group pcpqa >/dev/null || groupadd -r pcpqa
getent passwd pcpqa >/dev/null || \
  useradd -c "PCP Quality Assurance" -g pcpqa -d %{_testsdir} -M -r -s /bin/bash pcpqa 2>/dev/null
chown -R pcpqa:pcpqa %{_testsdir} 2>/dev/null
exit 0

%post testsuite
chown -R pcpqa:pcpqa %{_testsdir} 2>/dev/null
exit 0

%pre
getent group pcp >/dev/null || groupadd -r pcp
getent passwd pcp >/dev/null || \
  useradd -c "Performance Co-Pilot" -g pcp -d %{_localstatedir}/lib/pcp -M -r -s /sbin/nologin pcp
PCP_CONFIG_DIR=%{_localstatedir}/lib/pcp/config
PCP_SYSCONF_DIR=%{_confdir}
PCP_LOG_DIR=%{_logsdir}
PCP_ETC_DIR=%{_sysconfdir}
# rename crontab files to align with current Fedora packaging guidelines
for crontab in pmlogger pmie
do
    test -f "$PCP_ETC_DIR/cron.d/$crontab" || continue
    mv -f "$PCP_ETC_DIR/cron.d/$crontab" "$PCP_ETC_DIR/cron.d/pcp-$crontab"
done
# produce a script to run post-install to move configs to their new homes
save_configs_script()
{
    _new="$1"
    shift
    for _dir
    do
        [ "$_dir" = "$_new" ] && continue
        if [ -d "$_dir" ]
        then
            ( cd "$_dir" ; find . -type f -print ) | sed -e 's/^\.\///' \
            | while read _file
            do
                [ "$_file" = "control" ] && continue
                _want=true
                if [ -f "$_new/$_file" ]
                then
                    # file exists in both directories, pick the more
                    # recently modified one
                    _try=`find "$_dir/$_file" -newer "$_new/$_file" -print`
                    [ -n "$_try" ] || _want=false
                fi
                $_want && echo cp -p "$_dir/$_file" "$_new/$_file"
            done
        fi
    done
}
# migrate and clean configs if we have had a previous in-use installation
[ -d "$PCP_LOG_DIR" ] || exit 0	# no configuration file upgrades required
rm -f "$PCP_LOG_DIR/configs.sh"
for daemon in pmie pmlogger
do
    save_configs_script >> "$PCP_LOG_DIR/configs.sh" "$PCP_CONFIG_DIR/$daemon" \
        "$PCP_SYSCONF_DIR/$daemon"
done
for daemon in pmcd pmproxy
do
    save_configs_script >> "$PCP_LOG_DIR/configs.sh" "$PCP_SYSCONF_DIR/$daemon"\
        "$PCP_CONFIG_DIR/$daemon" /etc/$daemon /etc/sysconfig/$daemon
done
exit 0

%if !%{disable_microhttpd}
%preun webapi
if [ "$1" -eq 0 ]
then
%if !%{disable_systemd}
    systemctl --no-reload disable pmwebd.service >/dev/null 2>&1
    systemctl stop pmwebd.service >/dev/null 2>&1
%else
    /sbin/service pmwebd stop >/dev/null 2>&1
    /sbin/chkconfig --del pmwebd >/dev/null 2>&1
%endif
fi
%endif

%preun manager
if [ "$1" -eq 0 ]
then
%if !%{disable_systemd}
    systemctl --no-reload disable pmmgr.service >/dev/null 2>&1
    systemctl stop pmmgr.service >/dev/null 2>&1
%else
    /sbin/service pmmgr stop >/dev/null 2>&1
    /sbin/chkconfig --del pmmgr >/dev/null 2>&1
%endif
fi

%preun
if [ "$1" -eq 0 ]
then
    # stop daemons before erasing the package
    %if !%{disable_systemd}
	systemctl --no-reload disable pmlogger.service >/dev/null 2>&1
	systemctl --no-reload disable pmie.service >/dev/null 2>&1
	systemctl --no-reload disable pmproxy.service >/dev/null 2>&1
	systemctl --no-reload disable pmcd.service >/dev/null 2>&1

	systemctl stop pmlogger.service >/dev/null 2>&1
	systemctl stop pmie.service >/dev/null 2>&1
	systemctl stop pmproxy.service >/dev/null 2>&1
	systemctl stop pmcd.service >/dev/null 2>&1
    %else
	/sbin/service pmlogger stop >/dev/null 2>&1
	/sbin/service pmie stop >/dev/null 2>&1
	/sbin/service pmproxy stop >/dev/null 2>&1
	/sbin/service pmcd stop >/dev/null 2>&1

	/sbin/chkconfig --del pcp >/dev/null 2>&1
	/sbin/chkconfig --del pmcd >/dev/null 2>&1
	/sbin/chkconfig --del pmlogger >/dev/null 2>&1
	/sbin/chkconfig --del pmie >/dev/null 2>&1
	/sbin/chkconfig --del pmproxy >/dev/null 2>&1
    %endif
    # cleanup namespace state/flag, may still exist
    PCP_PMNS_DIR=%{_pmnsdir}
    rm -f "$PCP_PMNS_DIR/.NeedRebuild" >/dev/null 2>&1
fi

%if !%{disable_microhttpd}
%post webapi
chown -R pcp:pcp %{_logsdir}/pmwebd 2>/dev/null
%if !%{disable_systemd}
    systemctl condrestart pmwebd.service >/dev/null 2>&1
%else
    /sbin/chkconfig --add pmwebd >/dev/null 2>&1
    /sbin/service pmwebd condrestart
%endif
%endif

%post manager
chown -R pcp:pcp %{_logsdir}/pmmgr 2>/dev/null
%if !%{disable_systemd}
    systemctl condrestart pmmgr.service >/dev/null 2>&1
%else
    /sbin/chkconfig --add pmmgr >/dev/null 2>&1
    /sbin/service pmmgr condrestart
%endif

%post
PCP_LOG_DIR=%{_logsdir}
PCP_PMNS_DIR=%{_pmnsdir}
# restore saved configs, if any
test -s "$PCP_LOG_DIR/configs.sh" && source "$PCP_LOG_DIR/configs.sh"
rm -f $PCP_LOG_DIR/configs.sh

# migrate old to new temp dir locations (within the same filesystem)
migrate_tempdirs()
{
    _sub="$1"
    _new_tmp_dir=%{_tempsdir}
    _old_tmp_dir=%{_localstatedir}/tmp

    for d in "$_old_tmp_dir/$_sub" ; do
        test -d "$d" -a -k "$d" || continue
        cd "$d" || continue
        for f in * ; do
            [ "$f" != "*" ] || continue
            source="$d/$f"
            target="$_new_tmp_dir/$_sub/$f"
            [ "$source" != "$target" ] || continue
	    [ -f "$target" ] || mv -fu "$source" "$target"
        done
        cd && rmdir "$d" 2>/dev/null
    done
}
for daemon in mmv pmdabash pmie pmlogger
do
    migrate_tempdirs $daemon
done
chown -R pcp:pcp %{_logsdir}/pmcd 2>/dev/null
chown -R pcp:pcp %{_logsdir}/pmlogger 2>/dev/null
chown -R pcp:pcp %{_logsdir}/pmie 2>/dev/null
chown -R pcp:pcp %{_logsdir}/pmproxy 2>/dev/null
touch "$PCP_PMNS_DIR/.NeedRebuild"
chmod 644 "$PCP_PMNS_DIR/.NeedRebuild"
%if !%{disable_systemd}
    systemctl condrestart pmcd.service >/dev/null 2>&1
    systemctl condrestart pmlogger.service >/dev/null 2>&1
    systemctl condrestart pmie.service >/dev/null 2>&1
    systemctl condrestart pmproxy.service >/dev/null 2>&1
%else
    /sbin/chkconfig --add pmcd >/dev/null 2>&1
    /sbin/service pmcd condrestart
    /sbin/chkconfig --add pmlogger >/dev/null 2>&1
    /sbin/service pmlogger condrestart
    /sbin/chkconfig --add pmie >/dev/null 2>&1
    /sbin/service pmie condrestart
    /sbin/chkconfig --add pmproxy >/dev/null 2>&1
    /sbin/service pmproxy condrestart
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files -f base.list
#
# Note: there are some headers (e.g. domain.h) and in a few cases some
# C source files that rpmlint complains about. These are not devel files,
# but rather they are (slightly obscure) PMDA config files.
#
%doc CHANGELOG COPYING INSTALL README VERSION.pcp pcp.lsm

%dir %{_confdir}
%dir %{_pmdasdir}
%dir %{_datadir}/pcp
%dir %{_localstatedir}/lib/pcp
%dir %{_localstatedir}/lib/pcp/config
%dir %attr(0775,pcp,pcp) %{_tempsdir}
%dir %attr(0775,pcp,pcp) %{_tempsdir}/pmie
%dir %attr(0775,pcp,pcp) %{_tempsdir}/pmlogger
%dir %attr(0700,root,root) %{_tempsdir}/pmcd

%dir %{_datadir}/pcp/lib
%{_datadir}/pcp/lib/ReplacePmnsSubtree
%{_datadir}/pcp/lib/bashproc.sh
%{_datadir}/pcp/lib/lockpmns
%{_datadir}/pcp/lib/pmdaproc.sh
%{_datadir}/pcp/lib/rc-proc.sh
%{_datadir}/pcp/lib/rc-proc.sh.minimal
%{_datadir}/pcp/lib/unlockpmns

%dir %attr(0775,pcp,pcp) %{_logsdir}
%attr(0775,pcp,pcp) %{_logsdir}/pmcd
%attr(0775,pcp,pcp) %{_logsdir}/pmlogger
%attr(0775,pcp,pcp) %{_logsdir}/pmie
%attr(0775,pcp,pcp) %{_logsdir}/pmproxy
%{_localstatedir}/lib/pcp/pmns
%{_initddir}/pcp
%{_initddir}/pmcd
%{_initddir}/pmlogger
%{_initddir}/pmie
%{_initddir}/pmproxy
%if !%{disable_systemd}
%{_unitdir}/pmcd.service
%{_unitdir}/pmlogger.service
%{_unitdir}/pmie.service
%{_unitdir}/pmproxy.service
%endif
%{_mandir}/man5/*
%config(noreplace) %{_sysconfdir}/sasl2/pmcd.conf
%config(noreplace) %{_sysconfdir}/cron.d/pcp-pmlogger
%config(noreplace) %{_sysconfdir}/cron.d/pcp-pmie
%config %{_sysconfdir}/bash_completion.d/pcp
%config %{_sysconfdir}/pcp.env
%config %{_sysconfdir}/pcp.sh
%dir %{_confdir}/pmcd
%config(noreplace) %{_confdir}/pmcd/pmcd.conf
%config(noreplace) %{_confdir}/pmcd/pmcd.options
%config(noreplace) %{_confdir}/pmcd/rc.local
%dir %{_confdir}/pmproxy
%config(noreplace) %{_confdir}/pmproxy/pmproxy.options
%dir %{_confdir}/pmie
%config(noreplace) %{_confdir}/pmie/control
%dir %{_confdir}/pmlogger
%config(noreplace) %{_confdir}/pmlogger/control

%{_localstatedir}/lib/pcp/config/pmafm
%dir %attr(0775,pcp,pcp) %{_localstatedir}/lib/pcp/config/pmie
%{_localstatedir}/lib/pcp/config/pmie
%{_localstatedir}/lib/pcp/config/pmieconf
%dir %attr(0775,pcp,pcp) %{_localstatedir}/lib/pcp/config/pmlogger
%{_localstatedir}/lib/pcp/config/pmlogger/*
%{_localstatedir}/lib/pcp/config/pmlogconf
%{_localstatedir}/lib/pcp/config/pmlogrewrite
%dir %attr(0775,pcp,pcp) %{_localstatedir}/lib/pcp/config/pmda

%if 0%{?rhel} == 0 || 0%{?rhel} > 5
%{tapsetdir}/pmcd.stp
%else				# rhel5
%ifarch ppc ppc64
# no systemtap-sdt-devel
%else				# ! ppc
%{tapsetdir}/pmcd.stp
%endif				# ppc
%endif

%files conf
%dir %{_includedir}/pcp
%{_includedir}/pcp/builddefs
%{_includedir}/pcp/buildrules
%config %{_sysconfdir}/pcp.conf

%files libs
%{_libdir}/libpcp.so.3
%{_libdir}/libpcp_gui.so.2
%{_libdir}/libpcp_mmv.so.1
%{_libdir}/libpcp_pmda.so.3
%{_libdir}/libpcp_trace.so.2
%{_libdir}/libpcp_import.so.1

%files libs-devel -f devel.list
%{_libdir}/libpcp.so
%{_libdir}/libpcp_gui.so
%{_libdir}/libpcp_mmv.so
%{_libdir}/libpcp_pmda.so
%{_libdir}/libpcp_trace.so
%{_libdir}/libpcp_import.so
%{_includedir}/pcp/*.h
%{_datadir}/pcp/examples

# PMDAs that ship src and are not for production use
# straight out-of-the-box, for devel or QA use only.
%{_pmdasdir}/simple
%{_pmdasdir}/sample
%{_pmdasdir}/trivial
%{_pmdasdir}/txmon

%files testsuite
%defattr(-,pcpqa,pcpqa)
%{_testsdir}

%if !%{disable_microhttpd}
%files webapi
%{_initddir}/pmwebd
%if !%{disable_systemd}
%{_unitdir}/pmwebd.service
%endif
%{_libexecdir}/pcp/bin/pmwebd
%attr(0775,pcp,pcp) %{_logsdir}/pmwebd
%{_confdir}/pmwebd
%config(noreplace) %{_confdir}/pmwebd/pmwebd.options
# duplicate directories from pcp and pcp-webjs, but rpm copes with that.
%dir %{_datadir}/pcp
%dir %{_datadir}/pcp/webapps
%{_mandir}/man1/pmwebd.1*
%{_mandir}/man3/PMWEBAPI.3*
%endif

%files webjs
# duplicate directories from pcp and pcp-webapi, but rpm copes with that.
%dir %{_datadir}/pcp
%dir %{_datadir}/pcp/webapps
%{_datadir}/pcp/webapps/*.png
%{_datadir}/pcp/webapps/*.ico
%{_datadir}/pcp/webapps/*.html
%{_datadir}/pcp/webapps/blinkenlights

%files webapp-grafana
%dir %{_datadir}/pcp
%dir %{_datadir}/pcp/webapps
%{_datadir}/pcp/webapps/grafana

%files webapp-graphite
%dir %{_datadir}/pcp
%dir %{_datadir}/pcp/webapps
%{_datadir}/pcp/webapps/graphite

%files webapp-vector
%dir %{_datadir}/pcp
%dir %{_datadir}/pcp/webapps
%{_datadir}/pcp/webapps/vector

%files manager
%{_initddir}/pmmgr
%if !%{disable_systemd}
%{_unitdir}/pmmgr.service
%endif
%{_libexecdir}/pcp/bin/pmmgr
%attr(0775,pcp,pcp) %{_logsdir}/pmmgr
%config(missingok,noreplace) %{_confdir}/pmmgr
%config(noreplace) %{_confdir}/pmmgr/pmmgr.options
%{_mandir}/man1/pmmgr.1*

%files import-sar2pcp
%{_bindir}/sar2pcp
%{_mandir}/man1/sar2pcp.1*

%files import-iostat2pcp
%{_bindir}/iostat2pcp
%{_mandir}/man1/iostat2pcp.1*

%files import-mrtg2pcp
%{_bindir}/mrtg2pcp
%{_mandir}/man1/mrtg2pcp.1*

%files import-ganglia2pcp
%{_bindir}/ganglia2pcp
%{_mandir}/man1/ganglia2pcp.1*

%files import-collectl2pcp
%{_bindir}/collectl2pcp
%{_mandir}/man1/collectl2pcp.1*

%if !%{disable_papi}
%files pmda-papi
%{_pmdasdir}/papi
%{_mandir}/man1/pmdapapi.1*
%endif

%if !%{disable_perfevent}
%files pmda-perfevent
%{_pmdasdir}/perfevent
%config(noreplace) %{_pmdasdir}/perfevent/perfevent.conf
%{_mandir}/man1/perfalloc.1*
%{_mandir}/man1/pmdaperfevent.1*
%{_mandir}/man5/perfevent.conf.5*
%endif

%if !%{disable_infiniband}
%files pmda-infiniband
%{_pmdasdir}/ib
%{_pmdasdir}/infiniband
%{_mandir}/man1/pmdaib.1*
%endif

%files -n perl-PCP-PMDA -f perl-pcp-pmda.list

%files -n perl-PCP-MMV -f perl-pcp-mmv.list

%files -n perl-PCP-LogImport -f perl-pcp-logimport.list

%files -n perl-PCP-LogSummary -f perl-pcp-logsummary.list

%if !%{disable_python2}
%files -n python-pcp -f python-pcp.list.rpm
%endif

%if !%{disable_python3}
%files -n python3-pcp -f python3-pcp.list.rpm
%endif

%if !%{disable_qt}
%files -n pcp-gui -f pcp-gui.list

%{_confdir}/pmsnap
%config(noreplace) %{_confdir}/pmsnap/control
%{_localstatedir}/lib/pcp/config/pmsnap
%{_localstatedir}/lib/pcp/config/pmchart
%{_localstatedir}/lib/pcp/config/pmafm/pcp-gui
%{_datadir}/applications/pmchart.desktop
%endif

%files -n pcp-doc -f pcp-doc.list

%changelog
* Wed Apr 15 2015 Nathan Scott <nathans@redhat.com> - 3.10.4-1
- Update to latest PCP, pcp-webjs and Vector sources.
- Packaging improvements after re-review (BZ 1204467)
- Start pmlogger/pmie independent of persistent state (BZ 1185755)
- Fix cron error reports for disabled pmlogger service (BZ 1208699)
- Incorporate Vector from Netflix (https://github.com/Netflix/vector)
a Sub-packages for pcp-webjs allowing choice and reducing used space.

* Wed Mar 04 2015 Dave Brolley <brolley@redhat.com> - 3.10.3-2
- papi 5.4.1 rebuild

* Mon Mar 02 2015 Dave Brolley <brolley@redhat.com> - 3.10.3-1
- Update to latest PCP sources.
- New sub-package for pcp-import-ganglia2pcp.
- Python3 support, enabled by default in f22 onward (BZ 1194324)

* Mon Feb 23 2015 Slavek Kabrda <bkabrda@redhat.com> - 3.10.2-3
- Only use Python 3 in Fedora >= 23, more info at
  https://bugzilla.redhat.com/show_bug.cgi?id=1194324#c4

* Mon Feb 23 2015 Nathan Scott <nathans@redhat.com> - 3.10.2-2
- Initial changes to support python3 as default (BZ 1194324)

* Fri Jan 23 2015 Dave Brolley <brolley@redhat.com> - 3.10.2-1
- Update to latest PCP sources.
- Improve pmdaInit diagnostics for DSO helptext (BZ 1182949)
- Tighten up PMDA termination on pmcd stop (BZ 1180109)
- Correct units for cgroup memory metrics (BZ 1180351)
- Add the pcp2graphite(1) export script (BZ 1163986)

* Mon Dec 01 2014 Nathan Scott <nathans@redhat.com> - 3.10.1-1
- New conditionally-built pcp-pmda-perfevent sub-package.
- Update to latest PCP sources.

* Tue Nov 18 2014 Dave Brolley <brolley@redhat.com> - 3.10.0-2
- papi 5.4.0 rebuild

* Fri Oct 31 2014 Nathan Scott <nathans@redhat.com> - 3.10.0-1
- Create new sub-packages for pcp-webjs and python3-pcp.
- Fix __pmDiscoverServicesWithOptions(1) codes (BZ 1139529)
- Update to latest PCP sources.

* Fri Sep 05 2014 Nathan Scott <nathans@redhat.com> - 3.9.10-1
- Convert PCP init scripts to systemd services (BZ 996438)
- Fix pmlogsummary -S/-T time window reporting (BZ 1132476)
- Resolve pmdumptext segfault with invalid host (BZ 1131779)
- Fix signedness in some service discovery codes (BZ 1136166)
- New conditionally-built pcp-pmda-papi sub-package.
- Update to latest PCP sources.

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.9.9-1.2
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.9-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Nathan Scott <nathans@redhat.com> - 3.9.9-1
- Update to latest PCP sources.

* Wed Jul 16 2014 Mark Goodwin <mgoodwin@redhat.com> - 3.9.7-1
- Update to latest PCP sources.

* Wed Jun 18 2014 Dave Brolley <brolley@redhat.com> - 3.9.5-1
- Daemon signal handlers no longer use unsafe APIs (BZ 847343)
- Handle /var/run setups on a temporary filesystem (BZ 656659)
- Resolve pmlogcheck sigsegv for some archives (BZ 1077432)
- Ensure pcp-gui-{testsuite,debuginfo} packages get replaced.
- Revive support for EPEL5 builds, post pcp-gui merge.
- Update to latest PCP sources.

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.4-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Nathan Scott <nathans@redhat.com> - 3.9.4-1
- Merged pcp-gui and pcp-doc packages into core PCP.
- Allow for conditional libmicrohttpd builds in spec file.
- Adopt slow-start capability in systemd PMDA (BZ 1073658)
- Resolve pmcollectl network/disk mis-reporting (BZ 1097095)
- Update to latest PCP sources.

* Tue Apr 15 2014 Dave Brolley <brolley@redhat.com> - 3.9.2-1
- Improve pmdarpm(1) concurrency complications (BZ 1044297)
- Fix pmconfig(1) shell output string quoting (BZ 1085401)
- Update to latest PCP sources.

* Wed Mar 19 2014 Nathan Scott <nathans@redhat.com> - 3.9.1-1
- Update to latest PCP sources.

* Thu Feb 20 2014 Nathan Scott <nathans@redhat.com> - 3.9.0-2
- Workaround further PowerPC/tapset-related build fallout.

* Wed Feb 19 2014 Nathan Scott <nathans@redhat.com> - 3.9.0-1
- Create new sub-packages for pcp-webapi and pcp-manager
- Split configuration from pcp-libs into pcp-conf (multilib)
- Fix pmdagluster to handle more volumes, fileops (BZ 1066544)
- Update to latest PCP sources.

* Wed Jan 29 2014 Nathan Scott <nathans@redhat.com> - 3.8.12-1
- Resolves SNMP procfs file ICMP line parse issue (BZ 1055818)
- Update to latest PCP sources.

* Wed Jan 15 2014 Nathan Scott <nathans@redhat.com> - 3.8.10-1
- Update to latest PCP sources.

* Thu Dec 12 2013 Nathan Scott <nathans@redhat.com> - 3.8.9-1
- Reduce set of exported symbols from DSO PMDAs (BZ 1025694)
- Symbol-versioning for PCP shared libraries (BZ 1037771)
- Fix pmcd/Avahi interaction with multiple ports (BZ 1035513)
- Update to latest PCP sources.

* Sun Nov 03 2013 Nathan Scott <nathans@redhat.com> - 3.8.8-1
- Update to latest PCP sources (simple build fixes only).

* Fri Nov 01 2013 Nathan Scott <nathans@redhat.com> - 3.8.6-1
- Update to latest PCP sources.
- Rework pmpost test which confused virus checkers (BZ 1024850)
- Tackle pmatop reporting issues via alternate metrics (BZ 998735)

* Fri Oct 18 2013 Nathan Scott <nathans@redhat.com> - 3.8.5-1
- Update to latest PCP sources.
- Disable pcp-pmda-infiniband sub-package on RHEL5 (BZ 1016368)

* Mon Sep 16 2013 Nathan Scott <nathans@redhat.com> - 3.8.4-2
- Disable the pcp-pmda-infiniband sub-package on s390 platforms.

* Sun Sep 15 2013 Nathan Scott <nathans@redhat.com> - 3.8.4-1
- Very minor release containing mostly QA related changes.
- Enables many more metrics to be logged for Linux hosts.

* Wed Sep 11 2013 Stan Cox <scox@redhat.com> - 3.8.3-2
- Disable pmcd.stp on el5 ppc.

* Mon Sep 09 2013 Nathan Scott <nathans@redhat.com> - 3.8.3-1
- Default to Unix domain socket (authenticated) local connections.
- Introduces new pcp-pmda-infiniband sub-package.
- Disable systemtap-sdt-devel usage on ppc.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 3.8.2-1.1
- Perl 5.18 rebuild

* Wed Jul 31 2013 Nathan Scott <nathans@redhat.com> - 3.8.2-1
- Update to latest PCP sources.
- Integrate gluster related stats with PCP (BZ 969348)
- Fix for iostat2pcp not parsing iostat output (BZ 981545)
- Start pmlogger with usable config by default (BZ 953759)
- Fix pmatop failing to start, gives stacktrace (BZ 963085)

* Wed Jun 19 2013 Nathan Scott <nathans@redhat.com> - 3.8.1-1
- Update to latest PCP sources.
- Fix log import silently dropping >1024 metrics (BZ 968210)
- Move some commonly used tools on the usual PATH (BZ 967709)
- Improve pmatop handling of missing proc metrics (BZ 963085)
- Stop out-of-order records corrupting import logs (BZ 958745)

* Tue May 14 2013 Nathan Scott <nathans@redhat.com> - 3.8.0-1
- Update to latest PCP sources.
- Validate metric names passed into pmiAddMetric (BZ 958019)
- Install log directories with correct ownership (BZ 960858)

* Fri Apr 19 2013 Nathan Scott <nathans@redhat.com> - 3.7.2-1
- Update to latest PCP sources.
- Ensure root namespace exists at the end of install (BZ 952977)

* Wed Mar 20 2013 Nathan Scott <nathans@redhat.com> - 3.7.1-1
- Update to latest PCP sources.
- Migrate all tempfiles correctly to the new tempdir hierarchy.

* Sun Mar 10 2013 Nathan Scott <nathans@redhat.com> - 3.7.0-1
- Update to latest PCP sources.
- Migrate all configuration files below the /etc/pcp hierarchy.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.10-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 28 2012 Nathan Scott <nathans@redhat.com> - 3.6.10-2
- Ensure tmpfile directories created in %%files section.
- Resolve tmpfile create/teardown race conditions.

* Mon Nov 19 2012 Nathan Scott <nathans@redhat.com> - 3.6.10-1
- Update to latest PCP sources.
- Resolve tmpfile security flaws: CVE-2012-5530
- Introduces new "pcp" user account for all daemons to use.

* Fri Oct 12 2012 Nathan Scott <nathans@redhat.com> - 3.6.9-1
- Update to latest PCP sources.
- Fix pmcd sigsegv in NUMA/CPU indom setup (BZ 858384)
- Fix sar2pcp uninitialised perl variable warning (BZ 859117)
- Fix pcp.py and pmcollectl with older python versions (BZ 852234)

* Fri Sep 14 2012 Nathan Scott <nathans@redhat.com> - 3.6.8-1
- Update to latest PCP sources.

* Wed Sep 05 2012 Nathan Scott <nathans@redhat.com> - 3.6.6-1.1
- Move configure step from prep to build section of spec (BZ 854128)

* Tue Aug 28 2012 Mark Goodwin <mgoodwin@redhat.com> - 3.6.6-1
- Update to latest PCP sources, see installed CHANGELOG for details.
- Introduces new python-pcp and pcp-testsuite sub-packages.

* Thu Aug 16 2012 Mark Goodwin <mgoodwin@redhat.com> - 3.6.5-1
- Update to latest PCP sources, see installed CHANGELOG for details.
- Fix security flaws: CVE-2012-3418 CVE-2012-3419 CVE-2012-3420 and CVE-2012-3421 (BZ 848629)

* Thu Jul 19 2012 Mark Goodwin <mgoodwin@redhat.com>
- pmcd and pmlogger services are not supposed to be enabled by default (BZ 840763) - 3.6.3-1.3

* Thu Jun 21 2012 Mark Goodwin <mgoodwin@redhat.com>
- remove pcp-import-sheet2pcp subpackage due to missing deps (BZ 830923) - 3.6.3-1.2

* Fri May 18 2012 Dan Hork <dan[at]danny.cz> - 3.6.3-1.1
- fix build on s390x

* Mon Apr 30 2012 Mark Goodwin - 3.6.3-1
- Update to latest PCP sources

* Thu Apr 26 2012 Mark Goodwin - 3.6.2-1
- Update to latest PCP sources

* Thu Apr 12 2012 Mark Goodwin - 3.6.1-1
- Update to latest PCP sources

* Thu Mar 22 2012 Mark Goodwin - 3.6.0-1
- use %%configure macro for correct libdir logic
- update to latest PCP sources

* Thu Dec 15 2011 Mark Goodwin - 3.5.11-2
- patched configure.in for libdir=/usr/lib64 on ppc64

* Thu Dec 01 2011 Mark Goodwin - 3.5.11-1
- Update to latest PCP sources.

* Fri Nov 04 2011 Mark Goodwin - 3.5.10-1
- Update to latest PCP sources.

* Mon Oct 24 2011 Mark Goodwin - 3.5.9-1
- Update to latest PCP sources.

* Mon Aug 08 2011 Mark Goodwin - 3.5.8-1
- Update to latest PCP sources.

* Fri Aug 05 2011 Mark Goodwin - 3.5.7-1
- Update to latest PCP sources.

* Fri Jul 22 2011 Mark Goodwin - 3.5.6-1
- Update to latest PCP sources.

* Tue Jul 19 2011 Mark Goodwin - 3.5.5-1
- Update to latest PCP sources.

* Thu Feb 03 2011 Mark Goodwin - 3.5.0-1
- Update to latest PCP sources.

* Thu Sep 30 2010 Mark Goodwin - 3.4.0-1
- Update to latest PCP sources.

* Fri Jul 16 2010 Mark Goodwin - 3.3.3-1
- Update to latest PCP sources.

* Sat Jul 10 2010 Mark Goodwin - 3.3.2-1
- Update to latest PCP sources.

* Tue Jun 29 2010 Mark Goodwin - 3.3.1-1
- Update to latest PCP sources.

* Fri Jun 25 2010 Mark Goodwin - 3.3.0-1
- Update to latest PCP sources.

* Thu Mar 18 2010 Mark Goodwin - 3.1.2-1
- Update to latest PCP sources.

* Wed Jan 27 2010 Mark Goodwin - 3.1.0-1
- BuildRequires: initscripts for %%{_vendor} == redhat.

* Thu Dec 10 2009 Mark Goodwin - 3.0.3-1
- BuildRequires: initscripts for FC12.

* Wed Dec 02 2009 Mark Goodwin - 3.0.2-1
- Added sysfs.kernel metrics, rebased to minor community release.

* Mon Oct 19 2009 Martin Hicks <mort@sgi.com> - 3.0.1-2
- Remove IB dependencies.  The Infiniband PMDA is being moved to
  a stand-alone package.
- Move cluster PMDA to a stand-alone package.

* Fri Oct 09 2009 Mark Goodwin <mgoodwin@redhat.com> - 3.0.0-9
- This is the initial import for Fedora
- See 3.0.0 details in CHANGELOG
