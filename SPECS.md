# Dataset Uploader Specification Document

**Mission:** 

Provide users with a no-code method that enables them to import datasets to the protocol. This will streamline power user workflows in data submission, leading to the addition of more unique triple submissions and data at scale.

**Glossary:** 

* The “Dataset Uploader” is hereby referred to as “the system.” 
* **Triple**: Tri-faceted and canoncial statement, e.g. "Golden is a Company" or "The (company) name is Golden."
* **Disambiguate**: The process in which data is attempted to be matched to an existing entity or triple in the Golden knowledge graph. 

## Product Requirements

### Index Page

- Upload a file (i.e. CSV) into the system
- UI for uploader to access and view all of *their own* files as spreadsheets. Should include overall statistics such as date uploaded, data imported, data finished (i.e. all verification tasks completed), and coins received (can be negative if more triples rejected).

### Spreadsheet View

- Spreadsheet view UI of uploaded files should include basic editing features, such as cell editing and column/row deletion.
- Pagination UI for users to navigate their data. Users should be able to select how many rows of data they would like to be shown per page. A conservative row limit can be implemented depending on the interface to ensure high performance. 
- If a data cell contains either the UUID or Golden entity page URL, the cell is automatically disambiguated to that entity.
- Assign a predicate to any column. Unassigned columns will be disregarded for disambiguation and import.
- Select which Entity Type the file pertains to.
- Ability to select columns for disambiguation
- Ability to set a "Primary" column for disambiguation
- Disambiguate data cells
    - Disambiguations should be editable to allow users to change a match to another result.
    - Have a “Disambiguate” button. Clicking the button brings up a dropdown of “Disambiguate Selected Columns”, “Disambiguate Name Predicate”, and “Disambiguate All” options. Upon triggering any of the buttons, disambiguations are made and either 1) the text in the cells are replaced with the top disambiguation result or 2) the top disambiguation is cleanly shown next to the raw text in a distinguishable fashion.
        - “Disambiguate Selected Predicates” button: 
        Upon triggering, the system attempts to disambiguate all selected columns simultaneously.
        - “Disambiguate Primary Predicate” button: 
        Upon triggering, the system attempts to disambiguate the Primary column based on 1) all other columns which have a predicate set if no columns are selected or 2) all selected columns.
        - “Disambiguate All” button: 
        Disambiguates all assigned columns. Upon triggering, the system starts with non-name or non-primary predicate columns and uses this information to provide a result for the Primary column. This method is faster but less accurate  than if the user disambiguates the non-name predicate columns first (i.e. if user may correct a non-name column match, they will want to disambiguate the name column after this).
- Select and set a column as the citation column of another column
- Submit button submits data to the protocol, sending it to the verification queue.

### File Statistics

Show a spreadsheet status “tracker” after upload on the Spreadsheet View and Index Page and highlight verified triples so the user knows which triples are still awaiting verification (no color) or have been accepted (green) or rejected (red). Example —> Triple Status: 5/100 accepted. 5/100 rejected. 90/100 pending.

## Technical Requirements

- System is tied to user’s dApp account and uses that account’s JWT token.
- As a minimum, the system must be able to upload CSV files.
- Disambiguation features make calls to Godel’s `disambiguate_triples` method
    - Accepts first match in list for each instance. UI displays name but backend is connected to UUID.
    - All matches retained for each instance so that the user may view or edit disambiguation
- Column assignments make calls to Godel’s `predicates` method or are inherently tied to it so that live predicate updates are made automatically. Example: If the MDTs of a predicate are updated, this should be reflected automatically.
- Submit button make calls to Godel’s methods for statement creation and submission.
    - For each row where the Name column is without a match, the row goes through `CreateEntityInput` then the API’s `create_entity`  method to submit the data together as entities.
    - For each row where the Name column has a match, each submitted data cell goes though `CreateStatementInput` then the API’s `create_statement` method to submit triples individually.
- Internal check to ensure all MDT columns are set when users click the Submit button before the the submit process is already performed.
- To ensure post-upload spreadsheet statuses are accurate, downstream responses are sent  to the spreadsheet when a triple is either accepted or rejected. The tracker and triple highlighting should be updated accordingly. Ideally, this would be done live but in batches is also acceptable.

## User Persona: The Accurate User

### Who are they?

These users are meticulous and are looking to expand the knowledge graph without human errors. They are most the most good faith users. 

### Why would they use the application?

They may be 1) utilizing the graph for their own research and education; 2) be worried about the negative implications of triple rejection; or 3) professionals using data for work projects. Data files are more likely to be moderate in size and they will want to check disambiguation matches. 

### What are they looking for?

They expect the system to be intuitive and for there to be various features related to ensuring data accuracy. 

### What problems may arise?

Since they will likely be spending a lot of time within a single file, they will want processes to require as few clicks as possible and for functions to properly operate (e.g. no lag between choosing a disambiguation and the UI updating). If the system isn’t fluid, they may stop using it out of frustration. 

### How does the system address their needs?

The system enables them to edit multiple entities from a central location. This type of user may use unassigned columns for personal reference and would use the multi-disambiguation step phrases to check and edit data. 

## User Persona: The Rapid User

### Who are they?

These users are looking to import the data fast and not too concerned about mild faults in the data (especially if the data is cited). They want to contribute and move to their next project as quickly as they can. 

### Why would they use the application?

They may be 1) interested in monetary or NFT gain; or 2) want to upload base (i.e. MDT) data and are relying on other users to fill in data fields that are more difficult to find. Data files are likely to be very large. They may or may not spot check disambiguation matches.

### What are they looking for?

They expect the system to function quickly and will be very interested in post-upload spreadsheet statuses to track progress and gains. 

### What problems may arise?

Since these users won’t thoroughly check their data before submission, the verification queue may be flooded with bad data. Extra extra checks would minimize the introduction of verification queue clogs.

### How does the system address their needs?

The system enables them to make bulk uploads without having to learn how to use Godel or programming. This type of user will likely, after setting the entity type and assigning columns, disambiguate all assigned columns at the same time, after which they quickly submit the data.  

## Existing Open Source Solution: Godel

### What is it

Users with datasets can quickly disambiguate and upload massive amounts of data. 

### What it does well

Users can set up scripts to upload their data in a highly scaleable way without having to rely on browsers or other software. 

### Why it’s not enough

Technical knowledge is necessary. Some users also prefer a more friendly and visual system to view and edit disambiguations via a UI. 

## The Suggested System

### Non-Functional Specs

Interface should be as intuitive and streamlined as possible without compromising functionality. The appearance should be clean and the learning curve low. 

### Presentation Layer

**Index Page:** 

There will be two large buttons titled “Upload File” and “View Previous Uploads”. User guides and reference links to predicate definitions, etc. are listed under the buttons.

**View Previous Uploads Page:**

- User can view all files they have uploaded as well as their statuses. User can toggle between overall stats or tracker stats (see earlier explanations) with the default view being the overall stats.
- Vertical ellipses are associated to each file. Upon triggering, a drop menu appears with less common features such as “Rename File.”
- Clicking on a file name leads to the Spreadsheet View of that file.

**Upload File Page:**

User is prompted to:
- Input a name for the file
- Select the file destination or drag a file to the area where this is prompted
- Select the Entity Type the file pertains to
- Specify whether the first row is the header row (relevant for CSVs). If the name of the header row matches a predicate name, assign to that predicate. Allow for multiple columns to have the same header name.
- Click the upload button to confirm file information. Doing so directs the user to a “Spreadsheet View” of their file.

**Spreadsheet View Page:**

- Small icon attached to each column header to select a predicate. Remains after a predicate is assigned so user can change the assignment.
- MDTs of their specified Entity Type are listed at the top of the page in red divs. Clicking one of these buttons directs the user to the predicate description page [as specified on the protocol schema page](https://dapp.golden.xyz/schema).
- Once an MDT predicate column is assigned, 1) its red MDT div at the top of the page is removed; and 2) that column is moved to the left (in a prominent position). The Name column, once set, should be the left-most column.
- Ideally, MDT columns will to stand out since this data is particularly important. Once an MDT column is assigned, an MDT section appears and expands with the MDTs that are assigned. Since MDT columns will all be to the left, the interface can be clean.
- Small icon attached to each data cell once disambiguations are made so user can click on it to remove or change the matched disambiguation
- A single citation column can be assigned to mulitple predicate columns
- Once a citation column is set, there should be some kind of indication showing the relationship between the columns, such as arrows pointing from the citation column to the cited column and moving the columns adjacent to each other.
- Features located above the spreadsheet data:
    - Columns missing citation information counter
    - Disambiguation options presented in a dropdown menu
    - Submit button. User is asked to confirm after triggering with a short message warning users about the implication of submitting incorrect data.
    - Tracking information once data is imported.
- After a user clicks on a disambiguation button, if they click on either the same disambiguation button or the “Disambiguate all” button, a warning is shown that if they made any changes that their current disambiguations may be replaced if they proceed.
- Pagination selection and options (to change number of rows shown) below the data.
- Post-upload, accepted triples should be highlighted in green and rejected triples in red so user can refer back to their spreadsheet to get a visual view of the statuses of their triples.

**Monitoring & Alerting** 

If a user is clearly not using the system correctly (e.g. user tries to import worksheet without disambiguating any cells), they are presented with a warning message before the event trigger is activated. Other misuses include not including a single citation column or uploading a file with the same name as an existing one.

## Risks and Assumptions

### Data Quality

After deployment, users will have the ability to mass upload any dataset. Initial monitoring of the system’s use is particularly vital to check gaming efforts. There may also be an influx of inappropriate or offensive data (particularly with urls or citations) into the graph. If checks are integrated into the system, appropriate action can be taken such as banning or warning users.

### Security

The system needs to be built with user data and privacy protection in mind. Depending on the how the system is built and thus run, the uploader itself will also need to handle potential malware threats. 

## Future Features

Below are features which have value but are non-essential for early versions. 

- Capability to upload multiple types of data (e.g. json, xlsx, numbers)
- Select a set of columns to isolate and edit on their own. The value of these columns are tied to the original spreadsheet but may be edited, disambiguated, and imported separately. This is particularly useful if wanting to import, for example, founder data and company data at the same time.
- Enable and toggle row numbers off and on
- Enable and toggle alternating row color off and on
- Sort rows by column
- Image preview on hover if url to an image
- Ability for users to create a new column under a predicate with a uniform value that conforms with the predicate’s restrictions
- Add an enhance feature which programmatically searches for and fills in social media data data points for rows that have “Website” data. Upon triggering, a script is run to crawl each website for social media datapoints if not already present. Existing social media values in the spreadsheet are not replaced. This means social media columns may be auto-generated.
- Ability to mark data as incorrect. User receives bounty/NFT proportion if data is verified as incorrect and removed.
- Custom formatting, including transformations such as splitting data cells based on conditions
- Cell formulas for aggregations, etc.
- Cell filtering
- Multiple worksheets within a single file
- User-facing analytics
- Mobile compatibility