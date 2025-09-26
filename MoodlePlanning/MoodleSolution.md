# Moodle Solution for Project Laboratory Course

This document outlines a comprehensive Moodle-based solution for managing a large-scale "Project Laboratory" course with ~500 students per semester, including topic selection, documentation submission, grading, and end-of-term presentations.

## 1. Topic Management and Student Selection

### Core Requirements
- Staff members publish topics with title, description, and enrollment limits
- Students choose exactly one topic
- Manage ~500 students across multiple topics

### Moodle Implementation

#### Option A: Custom Database Activity (Recommended)
**Plugin:** Database Activity (core Moodle module)

**Setup:**
1. Create a **Database activity** called "Project Topics"
2. Configure database fields:
   - **Topic Title** (Text field)
   - **Description** (Textarea field)
   - **Supervisor** (Text field - auto-populated from user profile)
   - **Max Students** (Number field)
   - **Current Enrollments** (Number field - calculated)
   - **Category/Department** (Menu field - optional)

3. **Template Configuration:**
   - **Add entry template:** Form for staff to submit topics
   - **List template:** Display all available topics with enrollment buttons
   - **Single template:** Detailed topic view with enrollment status

**Enrollment Logic:**
- Use **Database activity** with custom PHP code or JavaScript to:
  - Track current enrollments vs. maximum
  - Prevent students from enrolling in multiple topics
  - Show "Full" status when limit reached

#### Option B: Choice Activity with Limitations
**Plugin:** Choice Activity (core Moodle)

**Setup:**
1. Create multiple **Choice activities** grouped by department/area
2. Each choice option represents a topic
3. Set individual limits per option (topic)
4. Configure to allow only one response per student

**Limitations:**
- Less flexible for topic descriptions
- Limited to ~100 options per Choice activity (may need multiple activities)

#### Option C: Third-Party Plugin (Most Comprehensive)
**Recommended Plugin:** [Scheduler](https://moodle.org/plugins/mod_scheduler) or [Project Selection](https://github.com/academic-moodle-cooperation/moodle-mod_publication) if available

**Alternative Plugin:** Custom development using **Local Plugin** framework

## 2. Documentation and Grading System

### Core Requirements
- Document submission (PDF + PPTX)
- Supervisor grading
- Bulk grade export

### Moodle Implementation

#### Assignment Activity Setup
**Plugin:** Assignment Activity (core Moodle)

**Configuration:**
1. **Assignment Settings:**
   - **Submission types:** File submissions enabled
   - **Accepted file types:** `.pdf, .pptx, .ppt`
   - **Maximum files:** 2 (one document, one presentation)
   - **Maximum file size:** 50MB per file

2. **Grading Setup:**
   - **Grade type:** Point (0-100 or custom scale)
   - **Grading method:** Simple direct grading
   - **Grade category:** "Documentation" (weight: e.g., 60%)
   - **Blind marking:** Optional for fairness

3. **Workflow:**
   - **Assignment availability:** Open during final weeks
   - **Due date:** End of semester
   - **Cut-off date:** Hard deadline
   - **Require submission statement:** Yes

#### Advanced Grading with Rubrics
**Plugin:** Advanced Grading (core Moodle feature)

**Setup:**
1. **Create Rubric with criteria:**
   - Technical content quality (0-25 points)
   - Documentation clarity (0-25 points)
   - Innovation/creativity (0-25 points)
   - Presentation quality (0-25 points)

2. **Rubric Benefits:**
   - Consistent grading across supervisors
   - Detailed feedback per criterion
   - Automatic calculation of final scores

#### Grade Export
**Built-in Moodle Features:**
- **Gradebook Export:** Excel/CSV format with all student grades
- **Grade Categories:** Separate documentation, presentation, and final grades
- **Grade Letters:** Configurable grade boundaries (A, B, C, etc.)

## 3. End-of-Term Presentations Management

### Core Requirements
- Session-based presentations (max 9 students per session)
- Committee registration (2 staff members per session)
- Scoring and comments during presentations
- Results visible to student advisors

### Moodle Implementation

#### Option A: Scheduler Plugin (Highly Recommended)
**Plugin:** [Scheduler](https://moodle.org/plugins/mod_scheduler)

**Setup:**
1. **Create Scheduler Activity:** "Presentation Sessions"
2. **Configure Slots:**
   - Duration: 2-3 hours per session
   - Max bookings per slot: 9 students
   - Allow teachers to add notes/grades

3. **Session Management:**
   - **Session Creation:** Staff can create time slots with titles
   - **Committee Assignment:** Two teachers assigned per slot
   - **Student Booking:** Students select available sessions

4. **Scoring Integration:**
   - Link to Grade item for presentation scores
   - Comments field for detailed feedback
   - Automatic gradebook integration

#### Option B: Database + Workshop Combination
**Plugins:** Database Activity + Workshop Activity (both core Moodle)

**Setup Process:**

1. **Database Activity: "Presentation Sessions"**
   - Fields: Session Title, Date/Time, Available Spots, Registered Students
   - Templates: Allow staff to create sessions, students to register

2. **Workshop Activity: "Presentation Evaluation"**
   - **Assessment Strategy:** Rubric or Accumulative grading
   - **Evaluation Criteria:**
     - Presentation clarity (0-20 points)
     - Technical content (0-30 points)
     - Q&A handling (0-20 points)
     - Time management (0-10 points)
     - Overall impression (0-20 points)

3. **Committee Workflow:**
   - Committee members access Workshop as "Teachers"
   - Evaluate each student presentation in their session
   - Add detailed comments and scores

#### Option C: Custom Solution with Groups
**Plugins:** Groups (core) + Assignment + Database

**Implementation:**
1. **Create Groups:** One group per presentation session
2. **Group Assignment:** "Presentation Evaluation"
3. **Database Activity:** Session management and committee assignment
4. **Custom PHP/JavaScript:** Link groups to evaluation forms

## 4. Advanced Features: Peer Review System

### Core Requirements
- Students evaluate other presentations in their session
- Meta-evaluation: Students rate peer reviews
- Detection of low-quality reviews

### Moodle Implementation

#### Workshop Activity (Comprehensive Solution)
**Plugin:** Workshop Activity (core Moodle)

**Configuration:**
1. **Workshop Structure:**
   - **Submission Phase:** Students upload presentation materials
   - **Assessment Phase:** Peer evaluation of presentations
   - **Grading Evaluation Phase:** Students rate received peer reviews

2. **Assessment Strategy:**
   - **Accumulative Grading:** Multiple criteria with weights
   - **Assessment Form:**
     - Content quality (0-25 points)
     - Presentation skills (0-25 points)
     - Innovation (0-25 points)
     - Technical depth (0-25 points)

3. **Peer Review Quality Control:**
   - **Grade for Assessment:** Points for quality peer reviews
   - **Comparison with Teacher Grades:** Automatic detection of outliers
   - **Review of Reviews:** Meta-evaluation phase

4. **Advanced Settings:**
   - **Number of Reviews:** Each student reviews 3-4 peers
   - **Review Assignment:** Within same session group
   - **Anonymous Reviews:** Optional for honest feedback

#### Database Activity for Meta-Reviews
**Plugin:** Database Activity (core Moodle)

**Purpose:** Track peer review quality ratings

**Fields:**
- Reviewer ID
- Review Target ID  
- Review Quality Score (1-5 scale: Useless to Very Useful)
- Comments on Review Quality

## 5. System Architecture and Workflow

### Course Structure
```
Project Laboratory Course
├── Topic Selection (Database/Choice Activity)
├── Project Groups (Groups - one per topic)
├── Documentation Submission (Assignment)
├── Presentation Sessions (Scheduler/Database)
├── Presentation Evaluation (Workshop)
├── Peer Review Quality (Database)
└── Final Grades (Gradebook)
```

### User Roles and Permissions

#### Custom Roles Setup
1. **Topic Supervisor Role:**
   - Create/edit topics in Database activity
   - Grade assigned students' documentation
   - View presentation evaluations for their students
   - Access gradebook for their supervised projects

2. **Committee Member Role:**
   - Register for presentation sessions
   - Evaluate presentations in assigned sessions
   - View all presentations in their sessions

3. **Student Role:**
   - Select one topic (with enrollment limits)
   - Submit documentation
   - Register for presentation session
   - Evaluate peer presentations
   - Rate peer review quality

### Gradebook Configuration
```
Final Grade (100%)
├── Documentation (60%)
│   ├── Technical Content (15%)
│   ├── Written Quality (15%)
│   ├── Innovation (15%)
│   └── Presentation Materials (15%)
├── Presentation (30%)
│   ├── Committee Evaluation (25%)
│   └── Peer Evaluation Average (5%)
└── Peer Review Quality (10%)
    ├── Review Quality Score (5%)
    └── Meta-Review Participation (5%)
```

## 6. Required Plugins and Setup

### Essential Plugins
1. **Scheduler** - `mod_scheduler` (for presentation session management)
2. **Database** - Core Moodle (for topic management)
3. **Workshop** - Core Moodle (for peer reviews)
4. **Assignment** - Core Moodle (for documentation)
5. **Groups** - Core Moodle (for session organization)

### Optional Enhancement Plugins
1. **Grade Export Enhanced** - For advanced reporting
2. **Configurable Reports** - Custom reporting dashboards
3. **Mass Actions** - Bulk operations on users/grades
4. **Event Monitor** - Automated notifications and workflows

### Custom Development Needs
1. **Topic Selection Logic:** JavaScript/PHP for enrollment limits
2. **Committee Assignment Interface:** Custom form for session staffing
3. **Grade Aggregation Rules:** Custom calculations for complex weighting
4. **Notification System:** Automated emails for deadlines and assignments

## 7. Implementation Timeline

### Phase 1: Basic Setup (2-3 weeks)
- Configure course structure and user roles
- Set up topic selection system (Database activity)
- Create documentation assignment with rubrics
- Configure basic gradebook categories

### Phase 2: Presentation System (2-3 weeks)
- Install and configure Scheduler plugin
- Set up presentation evaluation system
- Create committee assignment workflow
- Test with small user group

### Phase 3: Peer Review Integration (2-3 weeks)
- Configure Workshop activity for peer reviews
- Set up meta-review system
- Integrate peer scores into gradebook
- Create quality control mechanisms

### Phase 4: Testing and Refinement (2-4 weeks)
- Full system testing with pilot group
- Performance optimization for 500+ users
- User training and documentation
- Backup and recovery procedures

## 8. Technical Considerations

### Performance Optimization
- **Database Indexing:** Optimize queries for large user base
- **Caching:** Enable Moodle caching for better performance
- **File Storage:** Configure external file storage for large submissions
- **Server Resources:** Ensure adequate hosting for concurrent users

### Backup and Security
- **Regular Backups:** Automated course backups before critical deadlines
- **User Data Protection:** GDPR-compliant data handling
- **Access Control:** Proper role-based permissions
- **Activity Logs:** Comprehensive logging for audit trails

### Integration Possibilities
- **Student Information System (SIS):** Auto-enrollment and grade passback
- **External Calendar:** Sync presentation sessions with institutional calendar
- **Plagiarism Detection:** Integration with Turnitin or similar services
- **Video Conferencing:** Embedded BigBlueButton for remote presentations

## 9. Success Metrics and Monitoring

### Key Performance Indicators
- **Topic Selection Efficiency:** Time from opening to full enrollment
- **Submission Compliance:** Percentage of on-time documentation submissions
- **Presentation Attendance:** Session utilization rates
- **Peer Review Quality:** Average quality ratings and participation
- **System Performance:** Response times during peak usage

### Reporting Dashboards
- **Supervisor Dashboard:** Track students, grades, and session assignments
- **Administrator Dashboard:** Overall course metrics and system health
- **Student Dashboard:** Personal progress, deadlines, and peer review status

This comprehensive solution leverages Moodle's core capabilities while addressing the specific needs of a large-scale project laboratory course. The modular approach allows for phased implementation and future enhancements based on user feedback and evolving requirements.
