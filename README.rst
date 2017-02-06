=======================
Ricecake
=======================



Description:
=======================
The purpose of ricecake is to create a simplified way to use ricecooker.
Ricecake allows for a simplified, readable way to construct tree nodes with meta data.
Using ricecake eliminates the needs to write .py file to upload content to a channel programatically.


Usage:
=======================
Simply run ricecake from bash or your command prompt by using: 

ricecake --token=<yourKolibriTokenID> pathway/to/folder

'<yourKolibriTokenID>' is replaced by your token assigned from contentworkshop.learningequality.org.

'pathway/to/folder' is replaced with the absolute OR local pathway to your content folder, where channelmetadata.ini is located.


Content Hierarchy Requirements:
=======================
Your content must all reside in one single root folder. For this example, we will call the root folder "US History".
/US History/ must contain a file called 'channelmetadata.ini'. The details of these '.ini' files will be discussed further on.
inside /US History/, next to /US History/channelmetadata.ini you place your Master Channel folder, in our case called 'My US History Channel'.
/US History/My US History Channel/ can now contain any style and subset of folders and files. The heirarchy format of any folders and files 
inside /US History/My US History/ will be reflected on your content workshop online.
**All sub folders of /US History/ MUST have a 'metadata.ini' file in them.**


Information on .ini Files:
=======================
The .ini files required by this module allow for much neater and consolidated metadata trees thans ricecooker's built in functionality allows on its own.
channelmetadata.ini simply carry's the information passed in the ricecooker.contruct_node() method.
each metadata.ini files holds the meta data for every object (file, folder, children to be downloaded online) for the folder that the .ini is located in.
The included 'ricecake_sample_channel' folder is fully structured and ready for channel upload. It can be used to understand how to fill in and used the .ini files for your project.
