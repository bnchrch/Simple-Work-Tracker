import time
import datetime
import sys
import os.path


def print_to_file(start, stop, time_worked, work_text, work_log):
    """
    This function formulates the line in the text file for the time chunk of work that was just performed
    """
    today = datetime.date.today()

    record = ' || %.2f || %.2f || %.4f hours || %s\n' % (start, stop, time_worked/3600, work_text)

    #if it is a new file you have the option to set a start time for the project
    #  and how many hours a week you want to work
    if not os.path.isfile(work_log):
        while True:
            option = raw_input('\nThis is a new log, would you like to specify a start date and a hours per week goal for the project? (y/n): ').lower()
            if option == 'y':
                date = raw_input('\nplease enter the start date of the project (dd-mm-yyyy): ')
                hours_per_week = raw_input('\nplease enter the number of hours you intend to work on the project per week: ')
                try:
                    datetime.datetime.strptime(date, '%d-%m-%Y')
                    if hours_per_week.isdigit():
                        f = open(work_log, 'a')
                        f.write('#! || ' + date + ':' + hours_per_week + '\n')
                        f.close()
                        break
                    else:
                        print "\nPlease enter a valid number for hours to work!\n"
                except ValueError:
                    print "\nPlease enter a valid date!\n"

            else:
                break


    f = open(work_log, 'a')
    print '\n\n' + today.strftime('%b-%d-%Y') + record
    f.write(today.strftime('%b-%d-%Y') + record)
    f.close()


def timer(work_log):
    """
    starts the timer on 'start'
    ends on 'stop'
    records the time between the calls and allows a user to specify what they worked on
    during the time spent
    """
    start = time.time()
    print '\nyou started working at %s\n' % time.ctime(int(start))

    input = raw_input("\ntype 'stop' to stop timer...\n")
    while (input != 'stop'):
        input = raw_input("\ntype 'stop' to stop timer...\n")
    work = raw_input("\nwhat'd you work on?\n")
    stop = time.time()
    print_to_file(start, stop, (stop-start), work, work_log)


def parse_log(work_log):
    """
    invoked with the status call:
    determines the total time a user has worked based on the entries in the work log
    if a project starttime and hours_per_week has been specified in the file it
    also informs the user of how much they have worked relative to their goal
    """
    f = open(work_log, 'r')
    contents = f.readlines()
    f.close()
    if contents[0].split(" || ")[0] == '#!':
        day_start_string, hours_per_week = contents[0].split(" || ")[1].split(':')
        hours_per_week = int(hours_per_week)
        day_start = datetime.datetime.strptime(day_start_string, '%d-%m-%Y')
        time_passed = datetime.datetime.now() - day_start
        hours_to_work = hours_per_week*(1 + (time_passed.days/7))
        contents = contents[1:]
        total = get_total(contents)
        print_status(total, hours_to_work)

    else:
        total = get_total(contents)
        print_status(total)


def get_total(contents):
    """
    gets the total hours worked from an array of lines
    """
    total = 0
    for line in contents:
        total += float(line.split(' || ')[3].split(' ')[0])

    return total


def print_status(total, hours_to_work=False):
    if hours_to_work:
        print "\n%f / %d  (%f)\n" % (total, hours_to_work, total-hours_to_work)

    else:
        print "\nHours worked in total: %f\n" % total


def show_log(work_log):
    """
    prints the work log to stdout
    """
    f = open(work_log, 'r')
    contents = f.readlines()
    print '\n'
    for line in contents:
        print line
    print '\n'
    f.close()


def main(argv):
    try:
        work_log = argv[1]

    except IndexError:
        print 'You must specify a path to an existing work log or where you would like one to be created'
        sys.exit()

    print "Usage\n" \
          "start: to start timer\n" \
          "exit: to exit program\n" \
          "status: to see how much you have worked relative to your goals\n" \
          "show: to print current worklog to stdout\n" \
          "change: to modify the path to your worklog\n"

    input = ''
    while input != 'exit':
        input = raw_input("\ntype 'start' to start timer...\n")
        if input == 'start':
            timer(work_log)
        elif input == 'status':
            parse_log(work_log)
        elif input == 'show':
            show_log(work_log)
        elif input == 'change':
            work_log = raw_input('\ntype in the path to the work log you would like to change to: ')
        else:
            print "\nCommand not recognized. start, exit, status, show or change are the commands you have available"

if __name__ == "__main__":
    main(sys.argv)
