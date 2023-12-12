import React from "react";
import "./App.css";
import Section from "./Section";
import StarRating from "./StarRating";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Toast from "react-bootstrap/Toast";
import Accordion from "react-bootstrap/Accordion";

class Course extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      expanded: false, // whether the course is expanded (i.e. description is shown) or not
      showToast: false, // whether to display the Toast that shows sections and subsections
    };
  }

  getSections() {
    // Maps the sections of the course to a list of Section components
    let sections = [];
    let course = this.props.courseKey;

    for (const section of Object.values(this.props.data.sections)) {
      sections.push(
        <Section
          key={section.number}
          data={section}
          courseKey={course}
          sectionKey={section.number}
        />
      );
    }

    return sections;
  }

  openToast() {
    // Open the Toast that shows sections and subsections
    this.setState({ showToast: true });
  }

  closeToast() {
    // Close the Toast that shows sections and subsections
    this.setState({ showToast: false });
  }

  setExpanded(value) {
    // Sets the expanded state of the course
    this.setState({ expanded: value });
  }

  getCourseButton() {
    // Returns a button that adds/remove the course to/from the cart
    if (!this.props.cartCourses) return;

    let cartCourses = this.props.cartCourses;
    let course = this.props.data;

    let buttonOnClick = () => this.addCourse(course);
    let buttonText = "Add Course";
    let buttonColor = "teal"

    if (cartCourses.some((c) => c.number === course.number)) {
      buttonOnClick = () => this.removeCourse(course);
      buttonColor = "rgb(255, 168, 0)"
      buttonText = "Remove Course";
    }

    return (
      <Button 
      className="me-1" 
      variant="secondary" 
      onClick={buttonOnClick}
      style={{
        backgroundColor: buttonColor,
        color: "black",
      }}>
        {buttonText}
      </Button>
    );
  }

  getExpansionButton() {
    // Returns a button that expands/collapses the course description
    let buttonText = this.state.expanded ?  "▲" :  "▼";
    let buttonOnClick = () => this.setExpanded(!this.state.expanded);

    return (
      <Button
        variant="outline-dark"
        onClick={buttonOnClick}
      >
        {buttonText}
      </Button>
    );
  }

  addCourse = () => {
    // Adds the course to the cart
    this.props.addCartCourse(this.props.data);
  };

  removeCourse(course) {
    // Removes the course from the cart
    this.props.removeCartCourse(course);
  }

  getRequisites() {
    // Returns the requisites of the course as a formatted string
    let requisites = this.props.data.requisites;
    let reqList = [];
    let reqString = "";

    if (requisites.length > 0) {
      requisites.forEach((req) => {
        reqList.push("(" + req.join(" OR ") + ")");
      });
    } else {
      reqList.push("None");
    }
    reqString = reqList.join(" AND ");

    return reqString;
  }

  getKeywords() {
    // Returns the keywords of the course as a formatted string
    return this.props.data.keywords.join(", ");
  }

  showStarRating() {
    // Shows the star rating if it's under Completed Courses tab
    if (this.props.ratingMode === true) {
      return (
        <StarRating data={this.props.data} setRating={this.props.setRating} />
      );
    }
  }

  render() {
    let course = this.props.data.number;
    let name = this.props.data.name;
    let credits = this.props.data.credits;
    let description = this.props.data.description;
    if(this.props.expandedCourse){
      return (
        

        <Card className="col-auto mb-2 p-2 w-100">
          <Card.Title className="d-flex justify-content-between">
            {name} 
            <div>
              {this.getCourseButton()}
              {this.getExpansionButton()}
            </div>
          </Card.Title>
          <Card.Subtitle className="mb-2 text-muted">
            {course} · {credits + " Credits"}
          </Card.Subtitle>

          {this.state.expanded && <p>{description}</p>}

          {!this.props.compactView && (
            <>
              <span><strong>Requisites: </strong> {this.getRequisites()}</span>
              <span>
                <u>Keywords:</u> {this.getKeywords()}
              </span>
            </>
          )}

          {/* Completed courses do not have sections/subsections */}
          {!this.props.ratingMode && (
            <Button 
            className="mt-2" 
            variant="dark" 
            size="md"
            onClick={() => this.openToast()}
            style= {{
              position: "relative",
              backgroundColor: "teal",
              // justifyContent: "left",
              // alignItems: "left",
              textAlign: "left",
              width: "fit-content",
              padding: "4px",
              color: "black"
            }}>

              View Sections and Subsections
            </Button>
          )}

          {/* Star ratings are only shown when it's rendered under Completed Courses tab */}
          {this.showStarRating()}

          {/* Toast that shows sections and subsections */}
          <Toast
            show={this.state.showToast}
            onClose={() => this.closeToast()}
            style={{
              backgroundColor: "grey",
            }}
          >
            <Toast.Header
            style = {{
              color: "black",
              display: "flex",
              justifyContent: "flex-start"
            }}>
              <strong>{this.props.data.name}</strong>
              <small></small>
              
            </Toast.Header>

            <Toast.Body defaultActiveKey={this.props.data.sections[0].number}>
              <Accordion defaultActiveKey={this.props.data.sections[0].number}>
                {this.getSections()}
              </Accordion>
            </Toast.Body>

            {/* <Toast.Footer>
              <Button variant="secondary" onClick={() => this.closeToast()}>
                Close
              </Button>
            </Toast.Footer> */}
          </Toast>
        </Card>
      );
    }
    else{

    
      return (
        
      
        <Card className="col-auto mb-2 p-2">
          <Card.Title className="d-flex justify-content-between">
            {name} 
            <div>
              {this.getCourseButton()}
              {this.getExpansionButton()}
            </div>
          </Card.Title>
          <Card.Subtitle className="mb-2 text-muted">
            {course} · {credits + " Credits"}
          </Card.Subtitle>

          {this.state.expanded && <p>{description}</p>}

          {!this.props.compactView && (
            <>
              <span><strong>Requisites: </strong> {this.getRequisites()}</span>
              <span>
                <u>Keywords:</u> {this.getKeywords()}
              </span>
            </>
          )}

          {/* Completed courses do not have sections/subsections */}
          {!this.props.ratingMode && (
            <Button 
            className="mt-2" 
            variant="dark" 
            size="md"
            onClick={() => this.openToast()}
            style= {{
              position: "relative",
              backgroundColor: "teal",
              // justifyContent: "left",
              // alignItems: "left",
              textAlign: "left",
              width: "fit-content",
              padding: "4px",
              color: "black"
            }}>

              View Sections and Subsections
            </Button>
          )}

          {/* Star ratings are only shown when it's rendered under Completed Courses tab */}
          {this.showStarRating()}

          {/* Toast that shows sections and subsections */}
          <Toast
            show={this.state.showToast}
            onClose={() => this.closeToast()}
            style={{
              backgroundColor: "grey",
            }}
          >
            <Toast.Header
            style = {{
              color: "black",
              display: "flex",
              justifyContent: "flex-start"
            }}>
              <strong>{this.props.data.name}</strong>
              <small></small>
              
            </Toast.Header>

            <Toast.Body defaultActiveKey={this.props.data.sections[0].number}>
              <Accordion defaultActiveKey={this.props.data.sections[0].number}>
                {this.getSections()}
              </Accordion>
            </Toast.Body>

            {/* <Toast.Footer>
              <Button variant="secondary" onClick={() => this.closeToast()}>
                Close
              </Button>
            </Toast.Footer> */}
          </Toast>
        </Card>
      );
    }
  }
}

export default Course;
