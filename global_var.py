duplicate = 0
inserted = 0
expired = 0
skipped = 0
deadline_Not_given = 0
fromdate = ''
todate = ''
On_Error = 0
Total = 0
Clicked = 0
QC_Tender = 0
Number_Of_Links = ''
Links = ''
Delete_From_database = 0


def Process_End():
    # print("Publish Date Was Dead")
    print("Total: ", Total)
    print('Duplicate: ', duplicate)
    print('Expired: ', expired)
    print('Inserted: ', inserted)
    print('Deadline Not given: ', deadline_Not_given)
    print('QC Tenders: ', QC_Tender)
