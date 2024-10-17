%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global _with_bootstrap 0

%global with_bootstrap %{!?_with_bootstrap:0}%{?_with_bootstrap:1}
%global without_bootstrap %{?_with_bootstrap:0}%{!?_with_bootstrap:1}


Summary:        ObjectWeb Ant task
Name:           objectweb-anttask
Version:        1.3.2
Release:        9.0%{?dist}
Epoch:          0

License:        LGPLv2+
URL:            https://forge.objectweb.org/projects/monolog/
BuildArch:      noarch
Source0:        http://download.forge.objectweb.org/monolog/ow_util_ant_tasks_1.3.2.zip
BuildRequires:  java-devel
BuildRequires:  ant >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.6

%if %{without_bootstrap}
BuildRequires:  asm2
Requires:       asm2
%endif
Requires:       ant

%description
ObjectWeb Ant task

%package        javadoc
Summary:        Javadoc for %{name}


%description    javadoc
Javadoc for %{name}.

%prep
%setup -c -q -n %{name}

# extract jars iff in bootstrap mode
%if %{without_bootstrap}
find . -name "*.class" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;
%endif

%build
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
export CLASSPATH=$(build-classpath asm2/asm2)
ant -Dbuild.compiler=modern -Dbuild.sysclasspath=first jar jdoc

%install
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 output/lib/ow_util_ant_tasks.jar\
 $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr output/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "%{name}" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/%{name}

%files
%doc doc/* 
%doc output/jdoc/*
%{_javadir}/*
%{_sysconfdir}/ant.d/*

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.3.2-5
- Adapt to current guidelines.
- Properly integrate with ant using /etc/ant.d.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-4.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.3.2-3.5
- Fix Group tags
- Fix Source0 URL.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-2.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3.2-1.4
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0:1.3.2-1jpp.3
- fix license tag

* Wed Aug 29 2007 Deepak Bhole <dbhole@redhat.com> 0:1.3.2-1jpp.2
- Remove distribution tag

* Mon Feb 12 2007 Tania Bento <tbento@redhat.com> 0:1.3.2-1jpp.1
- Changed %%BuildRoot tag.
- Bootstrap Buildling.
- Should not touch buildroot in %%prep.
- Removed %%Vendor tag.
- Removed %%Distribution tag.
- Fixed %%Release tag.
- Fixed %%Sourcei0 tag.
- Added %%doc to %%files section.
- Edited %%doc in %%files javadoc section.

* Thu Jul 20 2006 Ralph Apel <r.apel at r-apel.de> 0:1.3.2-1jpp
- First JPP-1.7 release
- Upgrade to 1.3.2, now requires asm2
- Add javadoc subpackage

* Mon Sep 20 2004 Ralph Apel <r.apel at r-apel.de> 0:1.2-1jpp
- First JPackage release
