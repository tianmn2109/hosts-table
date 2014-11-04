hosts-table
===========

Example:

         curl -s -L tianmn2109-OptiPlex-755:8000/collect | sh -s "name="mengnan.tian";position="18L02-3-10;badge=11568774" "


        you can upload your name, computer's positon and your badge number with the option argument -s and 
        "name="XXX";position="XXX";badge="XXX"", "name","position","badge" are optional, but they must be seperated by ';'.
         or just curl -s -L localhost:8000/collect | sh to collect your own computer's information.
