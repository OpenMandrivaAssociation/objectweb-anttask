%define section         free
%define gcj_support     1

Summary:        ObjectWeb Ant task
Name:           objectweb-anttask
Version:        1.3.2
Release:        %mkrel 3.0.9
Epoch:          0
Group:          Development/Java
License:        LGPL
URL:            http://forge.objectweb.org/projects/monolog/
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif
Source0:        http://download.fr2.forge.objectweb.org/monolog/ow_util_ant_tasks_%{version}.tar.bz2
Patch0:         objectweb-anttask-1.3.2-filesets.patch
BuildRequires:  ant
BuildRequires:  java-rpmbuild
BuildRequires:  xalan-j2
BuildRequires:  asm2
Provides:       owanttask = %{epoch}:%{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
ObjectWeb Ant task

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -c -q -n %{name}
%patch0 -p1
%remove_java_binaries

%build
export CLASSPATH=$(build-classpath xalan-j2 asm2/ )
export OPT_JAR_LIST=:
%{ant} jar jdoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 output/lib/ow_util_ant_tasks.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
pushd $RPM_BUILD_ROOT%{_javadir}
  ln -sf %{name}-%{version}.jar %{name}.jar
popd

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a output/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*.jar.*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}


%changelog
* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.2-3.0.7mdv2011.0
+ Revision: 607005
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.3.2-3.0.6mdv2010.1
+ Revision: 523452
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.3.2-3.0.5mdv2010.0
+ Revision: 426265
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.3.2-3.0.4mdv2009.1
+ Revision: 351640
- rebuild

* Fri Jan 25 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.3.2-3.0.3mdv2008.1
+ Revision: 157955
- BR asm2

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.3.2-3.0.1mdv2008.0
+ Revision: 87270
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Thu Aug 30 2007 David Walluck <walluck@mandriva.org> 0:1.3.2-3.0.0mdv2008.0
+ Revision: 76263
- BuildRequires: xalan-j2
- does not require asm2
- ship javadocs
- temporarily disable filesets (not supported on ant 1.7.0)

  + Adam Williamson <awilliamson@mandriva.org>
    - rebuild for 2008


* Thu Aug 24 2006 David Walluck <walluck@mandriva.org> 0:1.3.2-2mdv2007.0
- rebuild

* Mon Jul 24 2006 David Walluck <walluck@mandriva.org> 0:1.3.2-1mdv2007.0
- 1.3.2
- requires asm2 (circular)
- does not require xalan-j2

* Mon Jun 05 2006 David Walluck <walluck@mandriva.org> 0:1.2-1.2mdv2007.0
- rebuild for libgcj.so.7
- aot compile

* Sun May 29 2005 David Walluck <walluck@mandriva.org> 0:1.2-1.1mdk
- release

* Tue Sep 21 2004 Ralph Apel <r.apel at r-apel.de> 0:1.2-1jpp
- First JPackage release

