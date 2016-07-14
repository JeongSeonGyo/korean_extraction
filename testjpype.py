import jpype
import os

cpopt="-Djava.class.path=%s" % ("/usr/lib/jvm/java-7-openjdk-i386/jre/lib/i386/client/libjvm.so")

jpype.startJVM("/usr/lib/jvm/java-7-openjdk-i386/jre/lib/i386/client/libjvm.so","-ea","-Djava.class.path = %s" % os.path.abspath("."))

#print "JVM path:",getDefaultJVMPath()
print "classpath:",cpopt

jpype.java.lang.System.out.println("Hello World!!")
Test = jpype.JClass('Test')
t = Test()
#testPkg = jpype.JPackage('pkg')
#Test = testPkg.Test
#t = Test
t.speak("hi")
shutdownJVM()