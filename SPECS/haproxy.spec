%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_home    %{_localstatedir}/lib/haproxy
%define dist .el7

Summary: HA-Proxy is a TCP/HTTP reverse proxy for high availability environments
Name: haproxy
Version: 1.7.4
Release: 1%{?dist}
License: GPL
Group: System Environment/Daemons
URL: http://www.haproxy.org/
Source0: http://www.haproxy.org/download/1.7/src/%{name}-%{version}.tar.gz
Source1: %{name}.cfg
Source2: %{name}.service
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: pcre-devel make gcc openssl-devel 

Requires(pre):      shadow-utils
BuildRequires:      systemd-units
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
HA-Proxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
- route HTTP requests depending on statically assigned cookies
- spread the load among several servers while assuring server persistence
  through the use of HTTP cookies
- switch to backup servers in the event a main one fails
- accept connections to special ports dedicated to service monitoring
- stop accepting connections without breaking existing ones
- add/modify/delete HTTP headers both ways
- block requests matching a particular pattern

It needs very little resource. Its event-driven architecture allows it to easily
handle thousands of simultaneous connections on hundreds of instances without
risking the system's stability.

%prep
%setup -q

# We don't want any perl dependecies in this RPM:
%define __perl_requires /bin/true

%build
regparm_opts=
%ifarch %ix86 x86_64
regparm_opts="USE_REGPARM=1"
%endif

%{__make} %{?_smp_mflags} CPU="generic" TARGET="linux2628" USE_OPENSSL=1 USE_PCRE=1 USE_ZLIB=1 ${regparm_opts} ADDINC="%{optflags}" ADDLIB="%{__global_ldflags}" USE_LINUX_SPLICE=1 USE_CPU_AFFINITY=1 USE_PCRE_JIT=1

%install
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}
 
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -d %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -d %{buildroot}%{_sysconfdir}/rsyslog.d
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}
%{__install} -d %{buildroot}%{_sysconfdir}/%{name}/errors
%{__install} -d %{buildroot}%{_localstatedir}/log/%{name}
%{__install} -d %{buildroot}%{_mandir}/man1/
%{__install} -s %{name} %{buildroot}%{_sbindir}/
%{__install} -s %{name}-systemd-wrapper %{buildroot}%{_sbindir}/
%{__install} -p -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -c -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/
%{__install} -c -m 755 examples/errorfiles/*.http %{buildroot}%{_sysconfdir}/%{name}/errors/
%{__install} -c -m 755 doc/%{name}.1 %{buildroot}%{_mandir}/man1/

%clean
[ "%{buildroot}" != "/" ] && %{__rm} -rf %{buildroot}

%pre
getent group %{haproxy_group} >/dev/null || \
       groupadd -g 188 -r %{haproxy_group}
getent passwd %{haproxy_user} >/dev/null || \
       useradd -u 188 -r -g %{haproxy_group} -d %{haproxy_home} \
       -s /sbin/nologin -c "%{name}" %{haproxy_user}
exit 0
 
%post
%systemd_post %{name}.service
systemctl restart rsyslog.service


%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
systemctl restart rsyslog.service

%files
%defattr(-,root,root)
%doc CHANGELOG README examples/*.cfg doc/architecture.txt doc/configuration.txt doc/intro.txt doc/management.txt doc/proxy-protocol.txt
%doc %{_mandir}/man1/%{name}.1*
%dir %{_localstatedir}/log/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}
%attr(0755,root,root) %{_sbindir}/%{name}-systemd-wrapper
%attr(-,root,root) %{_unitdir}/%{name}.service
%dir %{_sysconfdir}/%{name}
%{_sysconfdir}/%{name}/errors
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg

%changelog
* Sun Jan 15 2017 David Bezemer <info@davidbezemer.nl>
- Update for HAproxy 1.6.11


