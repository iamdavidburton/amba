#!/usr/bin/env python3

import os
import csv
import sys
import time
import shutil
import argparse

################## COMMON TO BOTH AMBA AND IMBA MEMBERS #######################
class Members(object):
    def __init__(self):
        pass

    @property
    def members(self): # Dict used to store all members { <member_id>: AMBAMember_obj, ... }
        return self._members
    
    @property
    def emails(self): # Dict used to look up members by their email { <email>: <member_id>, ... }
        return self._emails
   
    def _map_fields(self, entry):
        """ Map fields from the first line of a CSV file
        """
        
        # First validate that the required fields exist
        for field in self._required_fields:
            if not field in entry:
                print("!!!Missing field -> %s in export file %s!!!" % (field, self._members_file))
                sys.exit()
        print(" - Required fields in %s have been validated." % (self._members_file))

        # Map expexted fields to their index locations 
        for i, field in enumerate(entry):
            self._fields[field.strip()] = i


################## AMBA MEMBERS ###############################################
class AMBAMembers(Members): # Inherite frrom Members
    def __init__(self, members_file):
        self._members_file = members_file
        self._members = dict() # { <member_id>: IMBAMember, ...}
        self._fields  = dict() # { <field>: <index>, ... }
        self._emails  = dict() # { <email>: <member_id>, ...}
        
        # Fields we expect to be in the AMBA members file
        self._required_fields = [ 
                'Membership ID', \
                'First name', \
                'Last name', \
                'Email', \
                'Phone', \
                'IMBA Member', \
                'Street Address', \
                'City', \
                'State', \
                'Postal Code', \
                'Latest Contribution Date', \
                'Latest Contribution Amount', \
                'Parent Membership ID', \
            ]

        # Parse and populate
        self._parse_members_file() 
    
    @property
    def required_fields(self):
        """ Make this public so that it can be used for writting
            out CSV files
        """
        return self._required_fields
    
    def _parse_members_file(self): 
        """  - Parse a AMBA member file
             - Create and populate AMBAMember objects
             - Add AMBAMember objects to AMBAMembers.members
             - Add each member email to AMBAMembers.emails
        """
        print(" Importing AMBA members from %s." % self._members_file)
        with open(self._members_file, 'r') as fd:
            data = fd.read()

        if data[:1] == '\ufeff': # Strip this off the front 
            data = data[1:]

        # Extract each entry and map it's fields to a member object
        for i, entry in enumerate(data.split("\n")):
            if len(entry) == 0: # Skip empty entries
                continue

            entry = entry.split(",") # Comma separated fields
            if i == 0: # First line is used to map fields
                self._map_fields(entry)
                continue # Skip to next entry after the fields are mapped

            am = AMBAMember()
            am.first_name = entry[self._fields["First name"]].strip().capitalize()
            am.last_name = entry[self._fields["Last name"]].strip().capitalize()

            am.street = entry[self._fields["Street Address"]].strip()
            am.city = entry[self._fields["City"]].strip().capitalize()
            am.state = entry[self._fields["State"]].strip().upper()
            am.postal_code = entry[self._fields["Postal Code"]].strip()
            
            am.email = entry[self._fields["Email"]].strip().lower()
            am.phone = entry[self._fields["Phone"]].strip()
            
            am.membership_id = entry[self._fields["Membership ID"]].strip()
            am.member_bundle_id = entry[self._fields["Parent Membership ID"]].strip()
            
            self._members[am.membership_id] = am # Members indexed here by membership id
            self._emails[am.email] = am.membership_id # A list to look up members by thier email

        print(" - %s AMBA members extracted from file %s."  % (len(self._members), self._members_file))

class AMBAMember(object):
    def __init__(self):
        self._first_name       = None
        self._last_name        = None
        self._street           = None
        self._city             = None
        self._state            = None
        self._postal_code      = None
        self._phone            = None
        self._email            = None
        self._membership_id    = None
        self._member_bundle_id = None # Used to link group members
        self._contrib_date     = None
        self._contrib_amount   = None
    
    def __str__(self):
        mstr = str()
        mstr += "\tAMBAMember:\n"
        mstr += "\t - Name:%s %s\n" % (self._first_name, self._last_name)
        mstr += "\t - Address:%s, %s, %s, %s\n" % (self._street, self._city, self._state, self._postal_code)
        mstr += "\t - Phone:%s\n" % self._phone
        mstr += "\t - Email:%s\n" % self._email
        mstr += "\t - Membership id:%s\n" % self._membership_id
        mstr += "\t - Bundle id:%s\n" % self._member_bundle_id
        mstr += "\t - Contribution:%s %s\n" % (self._contrib_date, self._contrib_amount)
        return mstr

    @property
    def first_name(self):
        return self._first_name
    @first_name.setter
    def first_name(self, value):
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name
    @last_name.setter
    def last_name(self, value):
        self._last_name = value

    @property
    def street(self):
        return self._street
    @street.setter
    def street(self, value):
        self._street = value

    @property
    def city(self):
        return self._city
    @city.setter
    def city(self, value):
        self._city = value
    
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value):
        self._state = value

    @property
    def postal_code(self):
        return self._postal_code
    @postal_code.setter
    def postal_code(self, value):
        self._postal_code = value

    @property
    def phone(self):
        return self._phone
    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, value):
        self._email = value
    
    @property
    def membership_id(self):
        return self._membership_id
    @membership_id.setter
    def membership_id(self, value):
        self._membership_id = value

    @property
    def member_bundle_id(self):
        return self._member_bundle_id
    @member_bundle_id.setter
    def member_bundle_id(self, value):
        self._member_bundle_id = value

    @property
    def contrib_date(self):
        return self._contrib_date
    @contrib_date.setter
    def contrib_date(self, value):
        self._contrib_date = value

    @property
    def contrib_amount(self):
        return self._contrib_amount
    @contrib_amount.setter
    def contrib_amount(self, value):
        self._contrib_amount = value


################## IMBA MEMBERS ###############################################
class IMBAMembers(Members): # Inherite frrom Members
    def __init__(self, members_file):
        self._members_file = members_file
        self._members      = dict() # { <member_id>: IMBAMember, ...}
        self._fields       = dict() # { <field>: <index>, ... }
        self._emails       = dict() # { <email>: <member_id>, ...}
        self._members_ay   = dict() # Auto-renew yearly members
        self._members_am   = dict() # Auto-renew montthly members
        self._members_reg  = dict() # Regular members (e.g. no auto-renew)

        # Fields we expect to be in the IMBA members file
        self._required_fields = [
            'Contact ID', \
            'First Name', \
            'Last Name', \
            'Street Address', \
            'City', \
            'State', \
            'Postal Code', \
            'Email', \
            'Phone', \
            'Membership ID', \
            'Membership Type', \
            'Membership Term', \
            'Auto-renew', \
            'Original Start Date (Since)', \
            'Current Start Date', \
            'End Date', \
            'Latest Contribution Date', \
            'Latest Contribution Amount', \
            'Membership Status', \
            'Parent Membership ID', \
        ]

        # Parse and populate
        self._parse_members_file() 

    @property
    def members_reg(self): # Regular members (e.g. not auto-renew)
        return self._members_reg
    @property
    def members_ay(self): # Auto-renew yearly members
        return self._members_ay
    @property
    def members_am(self): # Auto-renew monthly members
        return self._members_am         

    def _parse_members_file(self):
        """  - Parse a AMBA member file
             - Create and populate AMBAMember objects
             - Add IMBAMember objects to IMBAMembers.members
             - Add each member email to IMBAMembers.emails
        """
        print(" Importing IMBA members from %s." % self._members_file)
        with open(self._members_file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')

            # Extract each entry and map it's fields to a member object
            for entry in reader:  
                if reader.line_num == 1: # First line is used to map fields
                    self._map_fields(entry)
                    continue # Skip to next entry after the fields are mapped

                im = IMBAMember()
                im.first_name = entry[self._fields["First Name"]].strip().capitalize()
                im.last_name = entry[self._fields["Last Name"]].strip().capitalize()

                im.street = entry[self._fields["Street Address"]].strip()
                im.city = entry[self._fields["City"]].strip().capitalize()
                im.state = entry[self._fields["State"]].strip().upper()
                im.postal_code = entry[self._fields["Postal Code"]].strip()

                im.email = entry[self._fields["Email"]].strip().lower()
                im.phone = entry[self._fields["Phone"]].strip()

                im.membership_id = entry[self._fields["Membership ID"]].strip()
                im.member_bundle_id = entry[self._fields["Parent Membership ID"]].strip()
                
                im.member_type = entry[self._fields["Membership Type"]].strip().lower()
                im.member_term = entry[self._fields["Membership Term"]].strip().lower()
                im.auto_renew = entry[self._fields["Auto-renew"]].strip().lower()
                
                im.orig_start = entry[self._fields["Original Start Date (Since)"]].strip()
                im.curr_start = entry[self._fields["Current Start Date"]].strip()
                im.end_date = entry[self._fields["End Date"]].strip()
                
                im.contrib_date = entry[self._fields["Latest Contribution Date"]].strip()
                im.contrib_amount = entry[self._fields["Latest Contribution Amount"]].strip()

                if im.auto_renew == "yes": # Separate auto-renew members
                    if im.member_term == "month":
                        self._members_am[im.membership_id] = im

                    elif im.member_term == "year":
                        self._members_ay[im.membership_id] = im

                    else:
                        print("!!!ERROR Membership term is not month/year but is -> %s !!!" % im.member_term)
                        sys.exit()

                elif im.auto_renew == "no": # Regular members (e.g. no auto-renew)
                    self._members_reg[im.membership_id] = im

                else:
                    print("!!!ERROR Auto-renew term is not yes/no but is -> %s !!!" % im.auto_renew)
                    sys.exit()

                self._members[im.membership_id] = im # All members added to this list
                self._emails[im.email] = im.membership_id # A list to lookup memmbers by their email
    
        print(" - %s IMBA members extracted from file %s." % (len(self._members), self._members_file))
        print("   + %s regular members." % (len(self._members_reg)))
        print("   + %s auto-renew yearly members." % (len(self._members_ay)))
        print("   + %s auto-renew monthly members." % (len(self._members_am)))

class IMBAMember(AMBAMember): # Inherit from AMBAMember
    def __init__(self):
        # Fields that don't exist in AMBAMember class
        self._member_term = None
        self._auto_renew  = None
        self._orig_start  = None
        self._curr_start  = None
        self._end_date    = None

    def __str__(self):
        mstr = str()
        mstr += "\tIMBAMember:\n"
        mstr += "\t - Name:%s %s\n" % (self._first_name, self._last_name)
        mstr += "\t - Address:%s, %s, %s, %s\n" % (self._street, self._city, self._state, self._postal_code)
        mstr += "\t - Phone:%s\n" % self._phone
        mstr += "\t - Email:%s\n" % self._email
        mstr += "\t - Membership id:%s\n" % self._membership_id
        mstr += "\t - Bundle id:%s\n" % self._member_bundle_id
        mstr += "\t - Contribution:%s %s\n" % (self._contrib_date, self._contrib_amount)
        mstr += "\t - Auto-renew/term: %s / %s\n" % (self._auto_renew, self._member_term)
        mstr += "\t - Orig/current/end date: %s / %s / %s\n" % (self._orig_start, self._curr_start, self._end_date)
        return mstr

    @property
    def member_term(self):
        return self._member_term
    @member_term.setter
    def member_term(self, value):
        self._member_term = value
    
    @property
    def auto_renew(self):
        return self._auto_renew
    @auto_renew.setter
    def auto_renew(self, value):
        self._auto_renew = value

    @property
    def orig_start(self):
        return self._orig_start
    @orig_start.setter
    def orig_start(self, value):
        self._orig_start = value

    @property
    def curr_start(self):
        return self._curr_start
    @curr_start.setter
    def curr_start(self, value):
        self._curr_start = value
    
    @property
    def end_date(self):
        return self._end_date
    @end_date.setter
    def end_date(self, value):
        self._end_date = value

################## ALL MEMBERS ################################################
class AllMembers(object):
    """ Class to analyze both AMBA and IMBA members
        - Find duplicates
        - Export file with new members
    """

    def __init__(self, amba, imba, directory):
        print(" Analizing both sets of members")

        self._dir  = directory
        self._amba = amba
        self._imba = imba

        self._dup_ids = set()  # Duplicate member ids
        self._new_reg = list() # New regular memebers to add (e.g. no auto-renew)
        self._new_ay  = list() # New auto-renew yearly members
        self._new_am  = list() # New auto-renew montly members
        self._new_all = list() # All new members
        
        self._duplicate_members()  # Find duplicate members
        self._unique_members()     # Build dict of unique members
        self._output_new_members() # Output the new members

    def _duplicate_members(self):
        print(" - Looking for duplicate members, these will not be exported.")

        # Find duplicates base on membership id
        amba_ids = self._amba.members
        for imba_id in self._imba.members:
            if imba_id in amba_ids:
                #print("  + Duplicate member id %s")
                self._dup_ids.add(imba_id)

        # Find duplicates based on first and last name
        for imba_id in self._imba.members:
            fnamei = self._imba.members[imba_id].first_name.lower()
            lnamei = self._imba.members[imba_id].last_name.lower()
            namei = fnamei + lnamei

            for amba_id in self._amba.members:
                fnamea = self._amba.members[amba_id].first_name.lower()
                lnamea = self._amba.members[amba_id].last_name.lower()
                namea = fnamea + lnamea

                if namei == namea:
                    self._dup_ids.add(imba_id)
                    #print("   + Duplicate name: %s %s" % (self._imba.members[imba_id].first_name, self._imba.members[imba_id].last_name))

        
        # Find duplicates based on email
        for email in self._amba.emails: 
            if email in self._imba.emails:
                #print("   + Duplicate member email:%s" % email)
                a = self._amba.members[self._amba.emails[email]]
                i = self._imba.members[self._imba.emails[email]]
                #print(self._imba.members[self._imba.emails[email]])
                #print(self._amba.members[self._amba.emails[email]])
                #print("     AMBA info: %s %s %s " % (a.first_name, a.last_name, a.membership_id))
                #print("     IMBA info: %s %s %s orig:%s cur:%s exp:%s" % (i.first_name, i.last_name, i.membership_id, i.orig_start, i.curr_start, i.end_date))
                self._dup_ids.add(i.membership_id)

        print(" - %s duplicate members found. "  % len(self._dup_ids))
        print()

    def _unique_members(self):
        """ IMBA members that aren't already AMBA members
        """
        print(" - New members to add:")
        for imba_id in self._imba.members:
            if imba_id not in self._dup_ids: # Already an AMBA member
                member = self._imba.members[imba_id]
                
                self._new_all.append(member) # All new members
                print("   + %s %s (%s auto-renew:%s)" % (member.first_name, member.last_name, member.member_term, member.auto_renew))

                # Auto-rewnew monthly members
                if member.membership_id in self._imba.members_ay: 
                    self._new_ay.append(member)
                    
                # Auto-renew yearly members
                elif member.membership_id in self._imba.members_am: 
                    self._new_am.append(member)

                # Regular members 
                elif member.membership_id in self._imba.members_reg: 
                    self._new_reg.append(member)

        print()
        print(" - %s new membmers to add:" % len(self._new_all))
        print("   + %s regular members" % len(self._new_reg))
        print("   + %s auto yearly members" % len(self._new_ay))
        print("   + %s auto monthly members" % len(self._new_am))
        print()

    def _get_member_output(self, members):
        """ Given a list of members build the output string 
        """

        # Get the header from the required fields
        output = str()
        output += ",".join(self._amba.required_fields) 
        output += ","
        output += "Renewal due"
        output += "," 
        output += "Member since"
        output += "\n" 

        # Build the members string
        for member in members:
            output += member.membership_id    + ","
            output += member.first_name       + ","
            output += member.last_name        + ","
            output += member.email            + ","
            output += member.phone            + ","
            output += "Yes"                   + "," # All exported are IMBA members
            output += member.street           + ","
            output += member.city             + ","
            output += member.state            + ","
            output += member.postal_code      + ","
            output += member.contrib_date     + ","
            output += member.contrib_amount   + ","

            if member.member_bundle_id == "0": 
                output += "," # Leave blank if 0
            else:
                output += member.member_bundle_id + ","

            # If membership is renewed each month set the end date
            # to a year from the start date
            if member.member_term == "month":
                month,day,year = member.curr_start.split("/")
                year = int(year) + 1
                output += "%s/%s/%s," % (month,day,year)
            else:
                output += member.end_date + ","

            output += member.curr_start + ","

            output += "\n"

        return output

    def _output_new_members(self):
        """ Write the results to 3 separate files
            corresponding to membership renewal type
        """
        print(" - Output new members to files:")

        # All new members
        output = self._get_member_output(self._new_all)
        fname = os.path.join(self._dir, "new_all.csv")
        print("   + %s" % fname)
        with open(fname, 'w') as fd:
            fd.write(output)

        # Regular members file (e.g not auto-renew)
        output = self._get_member_output(self._new_reg)
        fname = os.path.join(self._dir, "new_reg.csv")
        print("   + %s" % fname)
        with open(fname, 'w') as fd:
            fd.write(output)

        # Auto-renew yearly members
        output = self._get_member_output(self._new_ay)
        fname = os.path.join(self._dir, "new_auto_year.csv")
        print("   + %s" % fname)
        with open(fname, 'w') as fd:
            fd.write(output)

        # Auto-renew montly members
        output = self._get_member_output(self._new_am)
        fname = os.path.join(self._dir, "new_auto_month.csv")
        print("   + %s" % fname)
        with open(fname, 'w') as fd:
            fd.write(output)


class Setup(object):
    def __init__(self, amba_file, imba_file):
        self._dir = os.path.join(os.getcwd(), time.strftime("%Y_%m_%d"))
        self._amba_file = os.path.join(self._dir, os.path.relpath(amba_file))
        self._imba_file = os.path.join(self._dir, os.path.relpath(imba_file))

    def __call__(self):
        if os.path.isdir(self._dir):
            print(" - %s already exists. Deleting ..." % self._dir)
            shutil.rmtree(self._dir)  

        print(" - Creating output directory %s" % self._dir)  
        os.mkdir(self._dir)

        print(" - Copying the membership files to the output directory.")
        shutil.copyfile(amba_file, self._amba_file)
        shutil.copyfile(imba_file, self._imba_file)

    @property
    def amba_file(self):
        return self._amba_file

    @property
    def imba_file(self):
        return self._imba_file

    @property
    def directory(self):
        return self._dir
    

################## MAIN #######################################################
if __name__ == "__main__":
    """ This program compares current IMBA members to current AMBA members.
        
        Current IMBA members that aren't AMBA members will be exported
        to 3 files corresponding to thier membership type:
          - Regular members (e.g. no auto-renew)
          - Auto-renew yearly members
          - Auto-renew monthly members

    """
    parser = argparse.ArgumentParser(description='Process AMBA & IMBA membership files')
    parser.add_argument('-a', '--amba', dest='amba_file', action='store', required=True,
                       help='AMBA membership file')
    parser.add_argument('-i', '--imba', dest='imba_file', action='store', required=True,
                       help='IMBA membership file')

    exit=False
    args = parser.parse_args()
    amba_file = os.path.abspath(args.amba_file)
    imba_file = os.path.abspath(args.imba_file)
    
    if not os.path.isfile(amba_file):
        print("Error: AMBA file %s not found." % amba_file)
        exit=True
    if not os.path.isfile(args.imba_file):
        print("Error: IMBA file %s not found." % imba_file)
        exit=True
    if exit:
        sys.exit()

    print(" - Found membership files")
    setup = Setup(amba_file, imba_file)
    setup()

    plen = 85
    print()
    print("*"*plen)
    print()
    
    am = AMBAMembers(setup.amba_file)
    print()
    print("-"*plen)
    print()
    
    im = IMBAMembers(setup.imba_file)
    print()
    print("-"*plen)
    print()

    AllMembers(amba=am, imba=im, directory=setup.directory)
    print()
    print("*"*plen)
    print()
