import React from "react";
import "./App.css";
import Tabs from "react-bootstrap/Tabs";
import Tab from "react-bootstrap/Tab";
import Sidebar from "./Sidebar";
import CourseArea from "./CourseArea";
import badgerLogo from "./BadgersLogo.png"
import helpIcon from "./helpIcon.png"
import Container from "react-bootstrap/Container";
import BadgersHelpLogo from "./BadgerHelpLogo.jpg";

/**
 * The main application component.
 *
 */
class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      allCourses: [], // All the courses fetched from the server.
      filteredCourses: [], // The courses to be displayed in the CourseArea under Search tab.
      subjects: [], // The list of unique subjects fetched from the server.
      completedCourses: [], // The list of completed courses.
      cartCourses: [], // The list of courses in the cart.
      showCart: true,
    };
  }


  /**
   * When the component mounts, fetch the classes data from the server.
   * Save the data in the state.
   *
   */
   componentDidMount() {
    // Fetch all the courses from the server
    fetch("https://cs571.cs.wisc.edu/api/react/classes")
      .then((res) => res.json())
      .then((data) => {
        this.setState({
          allCourses: data,
          filteredCourses: data,
          subjects: this.getSubjects(data),
        });

        return data;
      })
      .then((allCourses) => {
        // fetch all the completed courses
        fetch(
          "https://cs571.cs.wisc.edu/api/react/students/5022025924/classes/completed/"
        )
          .then((res) => res.json())
          .then((completedCourseNumbers) => {
            this.setState({
              completedCourses: completedCourseNumbers.data.map(
                (courseNumber) =>
                  allCourses.find((course) => course.number === courseNumber)
              ),
            });
          });
      })
      .catch((err) => console.log(err));
  }

  // Callback function that adds a new course to the cartCourses state
  addCartCourse = (course) => {
    // Duplicate check
    if (
      this.state.cartCourses.some(
        (cartCourse) => cartCourse.number === course.number
      )
    ) {
      console.log(`${course.number} is already in the cart`);
    } else {
      this.setState({
        cartCourses: [...this.state.cartCourses, course],
      });
    }
  };

  // Callback function that removes a course from the cartCourses state
  removeCartCourse(course) {
    this.setState({
      cartCourses: this.state.cartCourses.filter(
        (cartCourse) => cartCourse.number !== course.number
      ),
    });
  }

  getSubjects(data) {
    // Get all the subjects from the JSON of fetched courses.
    // Return a list of unique subjects.

    let subjects = [];
    subjects.push("All");

    for (const course of Object.values(data)) {
      if (subjects.indexOf(course.subject) === -1)
        subjects.push(course.subject);
    }

    return subjects;
  }

  // Callback function that sets the rating of a course
  setRating(courseNumber, rating) {
    this.setState({
      completedCourses: this.state.completedCourses.map((course) => {
        if (course.number === courseNumber) {
          course.rating = rating;
        }
        return course;
      }),
    });
  }

  // Returns the number of courses that are not rated yet.
  getNumCoursesNeedsRating() {
    const numRatedCourses = this.state.completedCourses.filter(
      (course) => course.rating !== undefined
    ).length;

    return this.state.completedCourses.length - numRatedCourses;
  }

  setCourses(courses) {
    // This is a callback function for the filteredCourses state.
    // Set the courses to be displayed in the CourseArea under Search tab.
    // Refer to the Sidebar component (Sidebar.js) to understand when this is used.
    this.setState({ filteredCourses: courses });
  }

  render() {
    return (
      <div key = "mainContainer" 
      style = {{
        backgroundColor: "rgb(88, 127, 150)",
      }}>
        <Tabs
          forceRenderTabPanel
          defaultActiveKey="search"
          style={{
            position: "fixed",
            zIndex: 1,
            width: "100%",
            backgroundColor: "rgb(197, 5, 12)",
            color:"black",        
          }}
        >
          {/* Search Tab */}
          <Tab eventkey = "badgerLogo" title={<img src ={badgerLogo} alt ="" width ="32" height="32"></img>}  disabled>
            
          </Tab>
          <Tab eventKey="search" tabClassName="tabColors" title="Search" 
          style={{ 
            paddingTop: "5vh",
          }}>
            <Sidebar
              setCourses={(courses) => this.setCourses(courses)}
              courses={this.state.allCourses}
              subjects={this.state.subjects}
            />
            <div style={{ marginLeft: "20vw"}}>
              <CourseArea
                data={this.state.filteredCourses}
                allData={this.state.allCourses}
                cartCourses={this.state.cartCourses}
                addCartCourse={this.addCartCourse.bind(this)}
                removeCartCourse={this.removeCartCourse.bind(this)}
                showCart={this.props.showCart}
              />
            </div>
            
          </Tab>

          {/* Cart Tab
          <Tab tabClassName="tabColors" eventKey="cart" title="Cart" 
          style={{ 
            paddingTop: "5vh",
            }}
          >
            <div style={{ marginLeft: "5vw" }}>
              <CourseArea
                data={this.state.filteredCourses}
                allData={this.state.allCourses}
                cartCourses={this.state.cartCourses}
                addCartCourse={this.addCartCourse}
                removeCartCourse={this.removeCartCourse.bind(this)}
                mode="cart"
              />
            </div>
          </Tab> */}

          {/* Completed Courses Tab */}
          <Tab
            eventKey="completedCourses"
            tabClassName="tabColors"
            title={`Completed Courses (${this.getNumCoursesNeedsRating()} needs rating)`}
            style={{ paddingTop: "5vh" }}
          >
            <div style={{ marginLeft: "5vw" }}>
              <CourseArea
                data={this.state.completedCourses}
                allData={this.state.allCourses}
                setRating={this.setRating.bind(this)}
                mode="completed"
              />
            </div>
          </Tab>
          
          

          <Tab eventKey="help" title={<img src ={helpIcon} alt ="" width ="32" height="32"></img>} className="to-right" tabClassName = "tabHelp">
            <Container fluid className="helpTab">
              <br>
              </br> 
              <br>
              </br> 
              <img src = {BadgersHelpLogo} alt = "" width="1500" height = "1000" className="rounded-circle"></img>
              <br>
              </br>
              <br>
              </br>
              This Website was made by Nikolaj Hindsbo using React Components. It was based on a project for CS571 at UW-Madison
              <br>
              </br>
              Navigate the website by using the tabs above, including "Search" and "Completed Courses" which are in the top left of the screen.
              <br>
              </br>
              To report any bugs, suggestions, or further questions, email me at Hindsbo@Wisc.edu
              <br>
              </br>
              Go Badgers!
            </Container>
          </Tab>
        </Tabs>
      </div>
    );
  }
}

export default App;
