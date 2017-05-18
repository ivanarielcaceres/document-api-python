############################################################
# Step 1)  Use Datasource object from the Document API and
#          add splitext to find file extension (twb*, tds*)
############################################################
from tableaudocumentapi import Workbook
from tableaudocumentapi import Datasource
from os.path import splitext
import re, sys

def print_info_workbook(file_name):
    ############################################################
    # Step 2)  Open the .twb or .twbx we want to inspect
    ############################################################
    sourceWB = Workbook(file_name)

    ############################################################
    # Step 3)  Print out all of the datasources on this workbook
    ############################################################
    print('----------------------------------------------------------')
    print('--- {} total datasources in this workbook'.format(len(sourceWB.datasources)))
    print('----------------------------------------------------------')

    ############################################################
    # Step 4)  Print the total field using on each datasource,
    #          the fields and what type they are
    ############################################################
    for key, value in enumerate(sourceWB.datasources):
        print('----------------------------------------------------------')
        print('--- {0} total fields in {1} datasource'.format(len(value.fields.values()), value.name))
        print('----------------------------------------------------------')

        print('----------------------------------------------------------')
        print('-- Info for our .tds:')
        print('--   name:\t{0}'.format(value.name))
        print('--   version:\t{0}'.format(value.version))
        print('----------------------------------------------------------')

        for connKey, connInfo in enumerate(value.connections):
            print('-------Connection #{0} - {1} ----------------------------'.format(connKey, connInfo))
            print ('Server: {}'.format(connInfo.server))
            print ('DbName: {}'.format(connInfo.dbname))
            print ('Username: {}'.format(connInfo.username))
            print('----------------------------------------------------------')

        for count, field in enumerate(value.fields.values()):
            print('{:>4}: {} is a {}'.format(count+1, field.name, field.datatype))
            blank_line = False
            if field.calculation:
                print('      the formula is {}'.format(field.calculation))
                blank_line = True
            if field.default_aggregation:
                print('      the default aggregation is {}'.format(field.default_aggregation))
                blank_line = True
            if field.description:
                print('      the description is {}'.format(field.description))

            if blank_line:
                print('')
        print('----------------------------------------------------------')

def print_info_ds(file_name):
    ############################################################
    # Step 2)  Open the .tds we want to inspect
    ############################################################
    sourceTDS = Datasource.from_file(file_name)

    ############################################################
    # Step 3)  Print out all of the fields and what type they are
    ############################################################
    print('----------------------------------------------------------')
    print('-- Info for our .tds:')
    print('--   name:\t{0}'.format(sourceTDS.name))
    print('--   version:\t{0}'.format(sourceTDS.version))
    print('----------------------------------------------------------')

    print('----------------------------------------------------------')
    print('--- {} total connections in this datasource'.format(len(sourceTDS.connections)))
    print('----------------------------------------------------------')

    for count, field in enumerate(sourceTDS.connections):
        print(field.dbname)
        print(field.server)
        print(field.username)
        print(field.authentication)

    ############################################################
    # Step 4)  Print the total field using on each datasource,
    #          the fields and what type they are
    ############################################################
    print('----------------------------------------------------------')
    print('--- {} total fields in this datasource'.format(len(sourceTDS.fields)))
    print('----------------------------------------------------------')
    for count, field in enumerate(sourceTDS.fields.values()):
        print('{:>4}: {} is a {}'.format(count+1, field.name, field.datatype))
        blank_line = False
        if field.calculation:
            print('      the formula is {}'.format(field.calculation))
            blank_line = True
        if field.default_aggregation:
            print('      the default aggregation is {}'.format(field.default_aggregation))
            blank_line = True
        if field.description:
            print('      the description is {}'.format(field.description))

        if blank_line:
            print('')
    print('----------------------------------------------------------')

def main():
    #Read filename passed (*.twb, *.twbx, *.tds, *.tdsx)
    full_file_name = sys.argv[1]
    file_name, extension = splitext(full_file_name)
    #Remove punctuation (eg: .twbx to twbx)
    extension = extension[1:]

    if (re.compile('twb.*').match(extension)):
        print_info_workbook(full_file_name)
    elif re.compile('tds.*').match(extension):
        print_info_ds(full_file_name)
    else:
        print("The file extension must be twb, twbx, tds or tdsx")

if __name__ == "__main__":
    main()
