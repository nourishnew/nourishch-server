from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage


# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up environment variables (replace these with your actual keys)

@app.route('/', methods=['GET'])
def server_status():
    return jsonify({'status': "running"})


@app.route('/answer', methods=['POST'])
def answer():
    
    data = request.json
    question = data.get('question')
    instruction ="""You are a helpful funny assistant that answers question about me under 100 words by 
    based on the context given between <context> tags ,stating the most relevant specific facts, bullet points and numbers 
    proving your answer and promotes me as a skilled candidate that they should hire.
    The question is asked by someone else such hiring manager or recruiter or a random person.
    Respond in third person
    using he/him/his to the user when talking about me.Be funny and enthusiastic and engaging while responding.
    If the question not professional or not regarding
    the person,ignore and respond in a funny and polite way or ask a funny question back.
    Response should be formatted in such a way that any title or paragraph is left aligned.
    Question is given between <questions> tags";
    """
    context = """
Overview:
I have extensive experience working at various software companies and on numerous projects,
which demonstrate my technical skills, leadership, communication, and problem-solving abilities.
I am always learning new technologies, reading research papers, and building projects to enhance my skills.
My expertise includes front-end and back-end development, machine learning, LLM app development,
Android development, distributed systems, computer security, advanced networking, Linux troubleshooting,
and concurrency. I practice LeetCode daily to improve my algorithmic skills. My goal is to work as a Production Engineer at Meta,
focusing on operating systems, networking, and problem-solving at scale.

Some important links are given below
Link to my website is www.nourishch.com
Link to my github is https://github.com/nourishnew.
Link to my LinkedIn is https://www.linkedin.com/in/nourish-cherish/
My email is ncherish@uwaterloo.ca.
My phone number is 647-456-6651.
Internships and Work Experience:

1. General Dynamics (May 2024 - April 2025) - AI Software Developer (London, Canada):
   - Implemented an LLM application using StreamlitPython, LangChain, Milvus DB Vector Store, and Llama 8B model, increasing accuracy by 90%.
   - Migrated ROS1 to ROS2 in python, reducing code by 25% and improving performance by 50%.
   - Developed an image recognition model with yolov8, increasing accuracy by 80% using pytorch,python, roboflow and yolov8.
   - Containerized different applications using Docker and integrated them with ISAACSIM.
   - Led an LLM project, designing and deploying it on company servers.Building a RAG application with company data that can answer
   questions specific to the company.
   -Skills learnt at General Dynamics include Pytorch, AI, machine learning, computer vision, ROS2, Docker,
   LLM, Langchain,llama index, Python,C++, leadership, communication, collaboration, Git, Jira, 
   confluence, bitbucket, colcon for building ROS.

2. Blackberry (Sep 2023 - Dec 2023) - QNX Embedded Software Developer (Ottawa):
   - Migrated open-source projects to QNX using C and CMake.
   - Wrote shell scripts for test binary management and integrated test results into the company’s automation environment.
   - Containerized development environments with Docker and used Terraform for repository management.
   - I was a QNX Embedded Software Developer intern ( Open source team) in Ottawa. Things I accomplished at Blackberry
   include Used C language and CMake to migrate open-source projects to QNX by making efficient code changes in the Make
   files and test scripts were used, and the software was tested on Raspberry PI and QNX emulator. 
   - Used GCC and GNU gnu to build open-source projects and integrated the tests into the company test automation environment allowing developers to see
   test results in a dashboard.
   -Used C/C++ and CMake to migrate open source C/C++ projects like azure iot-sdk, canDB, nano-msg,
   gtsam to QNX operating system and tested it on the target and emulator. Used qcc compiler to compile projects and utilized gdb
   to debug and solve test errors on the target.
   -Containerized the development environment using Docker enabling developers to build
   projects depending on the minimum cmake version required without affecting the host environment. I also used Terraform to import 
   public repos to the internal respository. 
   -Skills I learnt here include, C, C++, Cmake, RaspberryPi, Operating systems, board bring up,
   ssh, Terraform, Python, gdb.

3. Ultimate Kronos Group (Jan 2023 - April 2023) - Software Engineering Intern (Toronto, Canada):
   - Built a real-time data streaming service with Java Hibernate, Spring Boot, and RabbitMQ.
   - Improved Angular application performance and reduced bug reports by 30%.
   - This role included front-end and back-end development. Things I accomplished at Ultimate Kronos Group include Testing and
   debugging Angular application controller logic, backend REST API and SQL scripts resulting in a 30% reduction in user bug reports. 
   -Wrote a JavaScript program using Blob API to export user holidays in Excel format.
   -Implemented feature flags for newly implemented features using Spring Boot Java APIs that allow the production team to 
   enable/disable the feature by changing a Sql column value, resulting in 25% less time in bug fixing. 
   -I worked with Angular application modifying the front-end UI.I fixed bugs in controller logic. 
   -Skills I learnt here include Springboot, Java, Hibernate, RabbitMQ,SQL, TeamCity for Devops, Angular, Typescript.

4. Royal Bank of Canada (Jan 2022 - April 2022) - Software Developer Intern (Toronto, Canada):
   - Developed an internal data pipeline using Spring Boot, JPA, SQL, and Kafka.
   - Automated security token creation, reducing initialization time by 30%.
   - Wrote unit tests covering 89% of repository and database layers.
   -Things I accomplished at RBC includes Built an internal data pipeline using Spring boot, JPA,
   and Sql to fetch messages from the Kafka and store them in a Sql database, enabling the team
   to analyze production-level Kafka cluster issues 20% faster.
   -Skills i learnt here include Springboot, Java, JPA, Kafka, SQL, distributed system, unit testing Junit.

5. Ford Motor Company (May 2021 - Aug 2021) - Firmware Software Developer Intern (Toronto, Canada):
   - Implemented a kernel-level program in C to prevent memory partition removal, reducing board resets by 15%.
   - Developed shell scripts for boot-up mode identification and debugged bootloader issues.

6. Shomigo.com (Sep 2020 - Dec 2020) - Full-Stack Developer Intern (Toronto, Canada):
   - Led the development of front-end UIs and backend APIs using React.js, Express.js,and Neo4j, improving website responsiveness by 40%.
   -This was mostly a front-end development role. I built a lot of front-end UIs using React.js follwoing the design given in Figma.
   - I built Product page, feed page, Notifications, comments under products, CartPage,Settings page based on the Figma design
   provided to be by the designer and product manager.
   -Things I accomplished at Shomigo include ;Led the implementation of the Profile, Settings,
   Product and Cart page UI using React.js, HTML, and CSS, increasing website responsiveness by 40%
   and launched the beta version of the web application within 1 month of onboarding.
   -Developed backend API endpoints using Express.js and JavaScript Promises along with efficient
   cypher queries to fetch product information from the Neo4j graph database, resulting in 20% faster page load times.
   -I built backend REST Apis using Express.js, Node.js which interacts with neo4j graph database.

7. Kenna Technologies - Web Developer:
   - Improved user experience by redirecting users to fallback pages and migrated SQL scripts to accommodate updates.

Retail and Volunteer Experience:

1. Engineering Ambassador, University of Waterloo (2022 - 2023):
   - Represented the Faculty of Engineering, leading campus tours and informational sessions.
    -I Served as a student ambassador for the University of Waterloo’s Engineering Shadow program,
    representing the Faculty of Engineering to prospective high school students and faculties,
    offering guidance and answering questions about academic pathways, co-op opportunities and
    student life. 
    -Led campus tours and informational sessions for multiple students, providing
    insights into different engineering programs, student life and resources available at the university.
    Collaborated with faculty and staff to organize and execute different shadowing events, enhancing
    leadership and communication skills.

2. Sales Associate, Dollarama (2018 - 2019):
   - Handled customer purchases, managed inventory, and delivered exceptional service.

Software Projects:

1. Soccer Video Analysis System (Engineering Design Project):
   - Developed a web app using React.js and Fast API for extracting highlight clips from soccer videos, reducing latency by 90%.
   - Built a web app using React.js and Fast API to extract and play highlight clips such as goals, injuries,
   and referee scenes of a soccer footage video using a custom frame classification model trained using thousands
   of frames extracted from YouTube videos. 
   -I trained a custom machine learning model using AWS Sagemaker that can recognize
   if a particular fram of video is relevant or not. I trained it using frames of videos I downloaded from
   youtube videos and manually labelling them. 
   -I then built React web app that lets users upload a long
   soccer video. The video is sent to a FAST Api backend server. Ths server uses AWS sdk to upload the video to S3
   -S3 has a trigger which splits the videos into frames and each frame is sent for inference from the machine
   learning model deployed on sagemarker. Based on the inference results, clips are made highlighting different
   events such as goals, injuries, yellow card, red card. 
   -I wrote different AWS Lambdas for getting inference results in parallel using python concurrency. 
   -I deployed model on different servers increasing response time.
   -I decreased the frame rate extracted from videos to 1 frame per second. All of these decreased latency
   of pipeline by 90%. Finally, the resulting clips were stored in CDN and displayed to the users on the web app.
   - Link  to this project is https://github.com/nourishnew/soccer-highlights-frontend

2. Dojla (Cryptocurrency Trading Simulator):
   - Built a web app for cryptocurrency trading with React.js and Firebase, receiving 60 upvotes and 100s of signups in the first week.
   - Implemented authentication using Firebase Auth and React context and saved user and trading information on Firebase Cloud.
   - Deployed on Netlify and Received 60 upvotes and 100s of signups within the first week of the launch
   - Link to this project is www.dojla.com

3. Sorting Visualizer and Android App for Asteroids:
   - Demonstrated sorting algorithms and built an Android app displaying asteroid data using Kotlin and SQLite.

4. Tesla Apple CarPlay UI:
   - Created a Tesla screen UI using React.js, CSS.
   - Link to this project is https://teslascreen.netlify.app


5. OS Kernel:
   - Developed a real-time OS kernel with memory allocation and inter-process communication.
   
6. AI Saas APP:
   - Built a SaaS app using Next.js, tailWindCSS, Stripe, Prisma, mySQL and LLM APIs that allows users to generate different 
   medias such as code, music, video and conversations.
7. Personal Website:
    - Built a personal website using React.js, tailWindCSS and integrated a chatbot(me) using Langchain, gpt4, pinecone to answer questions related to my projects and experience.
    - Link to this project is www.nourishch.com
8. Movie Search app:
    - Built a movie search app using react.js, Javascript, react-query, axios that lets people search and add moveis to their watch list.
    - Link to this project is https://zearch-movie.netlify.app/
   

Certifications and Additional Skills:
- AWS Certified Cloud Practitioner
- OtherSkills: POS systems, cash handling, customer service, leadership, teamwork, problem-solving, ethical conduct, and communication.

I did my undergrad at the University of Waterloo in Computer engineering. I had 8 semesters. 
I took several courses to expand my knowledge in different areas of computer and software development.
Courses I took are given below.
List of courses I took in my undergrad are given below in each line.
Distributed computing,
Distributed systems,
ECE 105 Classical Mechanics ,
ECE 150 Fundamentals of Programming, 
ECE 190 Engineering Profession and Practice,
MATH 115 Linear Algebra for Engineering ,
MATH 117 Calculus 1 for Engineering ,
SPCOM 192 Communication in the Engineering Profession ,
COOP 1 Co-operative Work Term ,
PD 20 Engineering Workplace Skills, 
Developing Reasoned Conclusions ,
ECE 101A Work-term Reflections 1,
ECE 106 Electricity and Magnetism, 
ECE 108 Discrete Mathematics and Logic 1 ,
ECE 124 Digital Circuits and Systems ,
ECE 140 Linear Circuits ,
ECE 192 Engineering Economics and Impact on Society ,
MATH 119 Calculus 2 for Engineering ,
COOP 2 Co-operative Work Term ,
PD 21 Engineering Workplace Skills II: Developing Effective Plans ,
ECE 101B Work-term Reflections ,
ECE 109 Materials Chemistry for Engineers ,
ECE 204 Numerical Methods ,
ECE 205 Advanced Calculus 1 for Electrical and Computer Engineers ,
ECE 222 Digital Computers ,
ECE 240 Electronic Circuits 1 ,
ECE 250 Algorithms and Data Structures ,
COOP 3 Co-operative Work Term ,
PD 22 Professionalism and Ethics in Engineering Practice ,
ECE 101C Work-term Reflections ,
ECE 203 Probability Theory and Statistics 1 ,
ECE 207 Signals and Systems,
ECE 208 Discrete Mathematics and Logic 2 ,
ECE 224 Embedded Microprocessor Systems ,
ECE 252 Systems Programming and Concurrency ,
ECE 298 Instrumentation and Prototyping Laboratory ,
COOP 4 Co-operative Work Term 35. PD 8 Intercultural Skills,
Introductory of Earth sciences,
Digital Hardware systems,
real-time operating systems,
Analog control systems,
Probability theory and statistics,
COmpilers,
Database systems,
Computer Networks,
Foudation of Entreprenuership,
Introduction to  hydrology,
Engineering design project (FYDP)
Introduction to optimization,
Algorithm design and analysis,
Advanced topics in networking,
Fundamentals of computational intelligence and machine learning,
basic Human resource management,

"""
    print("query is")
    print(question)

    
    llm = ChatOpenAI(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-4o",
        temperature=0.0
    )

    # Combine the context and question to form the message
    message = f" Instruction: {instruction}\n\n<context> Context: {context} </context> \n\n<question> Question: {question} </question>"

    # Pass the message to the LLM to generate the answer
    response = llm([HumanMessage(content=message)])
    return jsonify({'answer': response.content})

if __name__ == '__main__':
    app.run(debug=True,port=5001)