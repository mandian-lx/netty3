%{?_javapackages_macros:%_javapackages_macros}

%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}

Name:           netty3
Version:        3.10.6
Release:        3.1
Summary:        An asynchronous event-driven network application framework and tools for Java
# CC0: src/main/java/org/jboss/netty/handler/codec/base64/Base64.java
Group:          Development/Java
License:        ASL 2.0 and BSD and CC0
URL:            http://netty.io/
Source0:        https://github.com/netty/netty/archive/netty-%{namedversion}.tar.gz

Patch0:         netty-3.10.6-port-to-jzlib-1.1.0.patch
Patch1:         disableNPN.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(ant-contrib:ant-contrib)
BuildRequires:  mvn(com.google.protobuf:protobuf-java)
BuildRequires:  mvn(com.jcraft:jzlib)
BuildRequires:  mvn(commons-logging:commons-logging)
BuildRequires:  mvn(io.netty:netty-tcnative)
BuildRequires:  mvn(javax.servlet:javax.servlet-api)
BuildRequires:  mvn(log4j:log4j:12)
BuildRequires:  mvn(org.apache.ant:ant)
BuildRequires:  mvn(org.apache.ant:ant-launcher)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.felix:org.osgi.compendium)
BuildRequires:  mvn(org.apache.felix:org.osgi.core)
BuildRequires:  mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires:  mvn(org.apache.maven.plugins:maven-resources-plugin)
BuildRequires:  mvn(org.bouncycastle:bcpkix-jdk15on)
BuildRequires:  mvn(org.jboss.logging:jboss-logging)
BuildRequires:  mvn(org.jboss.marshalling:jboss-marshalling)
BuildRequires:  mvn(org.slf4j:slf4j-api)
BuildRequires:  mvn(org.sonatype.oss:oss-parent:pom:)

Requires:       netty-tcnative
# src/main/java/org/jboss/netty/handler/codec/base64/Base64.java (unkown version)
Provides:       bundled(java-base64)

%description
Netty is a NIO client server framework which enables quick and easy
development of network applications such as protocol servers and
clients. It greatly simplifies and streamlines network programming
such as TCP and UDP socket server.

'Quick and easy' doesn't mean that a resulting application will suffer
from a maintainability or a performance issue. Netty has been designed
carefully with the experiences earned from the implementation of a lot
of protocols such as FTP, SMTP, HTTP, and various binary and
text-based legacy protocols. As a result, Netty has succeeded to find
a way to achieve ease of development, performance, stability, and
flexibility without a compromise.

%package javadoc
Summary:   API documentation for %{name}

%description javadoc
%{summary}.

%prep
%setup -q -n netty-netty-%{namedversion}

# just to be sure, but not used anyway
rm -rf jar doc license

%pom_remove_plugin :maven-jxr-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin org.eclipse.m2e:lifecycle-mapping
%pom_remove_dep javax.activation:activation
%pom_remove_plugin :animal-sniffer-maven-plugin
%pom_remove_dep :npn-api
%pom_xpath_remove "pom:extension[pom:artifactId[text()='os-maven-plugin']]"
%pom_xpath_remove "pom:execution[pom:id[text()='remove-examples']]"
%pom_xpath_remove "pom:plugin[pom:artifactId[text()='maven-javadoc-plugin']]/pom:configuration"
%pom_xpath_remove "pom:dependency[pom:artifactId[text()='netty-tcnative']]/pom:classifier"
#%% pom_xpath_remove "pom:dependency[pom:artifactId[text()='netty-tcnative']]/pom:scope"
# Set scope of optional compile dependencies to 'provided'
%pom_xpath_set "pom:dependency[pom:scope[text()='compile'] and pom:optional[text()='true']]/pom:scope" provided

# Force use servlet 3.1 apis
%pom_change_dep :servlet-api javax.servlet:javax.servlet-api:3.1.0

%pom_xpath_set "pom:dependency[pom:artifactId = 'log4j']/pom:version" 12

# Uneeded tasks
%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin :maven-source-plugin
# Unavailable plugin
%pom_remove_plugin kr.motd.maven:exec-maven-plugin
# Fix javadoc doclint
%pom_remove_plugin :maven-javadoc-plugin

sed s/jboss-logging-spi/jboss-logging/ -i pom.xml

# Remove bundled jzlib and use system jzlib
rm -r src/main/java/org/jboss/netty/util/internal/jzlib
%pom_add_dep com.jcraft:jzlib
sed -i s/org.jboss.netty.util.internal.jzlib/com.jcraft.jzlib/ \
    $(find src/main/java/org/jboss/netty/handler/codec -name \*.java | sort -u)
%patch0 -p1
%patch1 -p1

# adapting to excluded dep
rm -v src/main/java/org/jboss/netty/handler/ssl/JettyNpnSslEngine.java

%mvn_compat_version : %{version} 3.9.3 %{namedversion} 3.9.3.Final 3
%mvn_alias : org.jboss.netty:
%mvn_file  : %{name}

%build

# skipping tests because we don't have easymockclassextension
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc README.md
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt
 
%changelog
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 03 2016 gil cattaneo <puntogil@libero.it> 3.10.6-1
- update to 3.10.6.Final

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 08 2015 gil cattaneo <puntogil@libero.it> 3.9.3-3
- fix FTBFS rhbz#1239716
- fix URL field
- fix BR list and use BR mvn()-like
- switch to glassfish-servlet-api
- force log4j12
- remove duplicate files
- fix some rpmlint problem
- introduce license macro

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 12 2015 Marek Goldmann <mgoldman@redhat.com> - 3.9.3-1
- Rebuild to fix the release

* Thu Feb 12 2015 Jiri Vanek <jvanek@redhat.com> - 3.9.3-0
- Updated to netty 3.9.3
- uploaded sources netty-3.10.0.Final-dist.tar.bz2 and netty-3.9.3.Final-dist.tar.bz2
- added and applied patch1, disableNPN.patch
- modified patch0 netty-port-to-jzlib-1.1.0.patch
- release reset to 0
- added build requires java-devel and bouncycastle-pkix
- xpathed out npn-api and os-maven-plugin
- xpathed out from netty-tcnative  classifier and scope
- from sources removed JettyNpnSslEngine.java

* Tue Jun 10 2014 Michal Srb <msrb@redhat.com> - 3.6.6-4
- Rebuilt to fix provides

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 3.6.6-2
- Use Requires: java-headless rebuild (#1067528)

* Mon Dec 30 2013 Marek Goldmann <mgoldman@redhat.com> - 3.6.6-1
- Initial packaging of compat version 3 as a compat package

