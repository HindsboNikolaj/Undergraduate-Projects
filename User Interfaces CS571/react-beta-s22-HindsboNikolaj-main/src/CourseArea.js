import React from "react";
import "./App.css";
import Course from "./Course";
import Container from "react-bootstrap/Container";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";

class CourseArea extends React.Component {
  getCourses() {
    let courses = [];
    let cart =[];

    // if (this.props.mode === "cart") {
    //   // If the mode is cart, then we want to display the courses in the compact view.
    //   // They should also allow the user to remove the course from the cart.
    //   courses = this.props.cartCourses.map((course) => (
    //     <Course
    //       key={course.number}
    //       data={course}
    //       compactView={true}
    //       cartCourses={this.props.cartCourses}
    //       addCartCourse={this.props.addCartCourse}
    //       removeCartCourse={(data) => this.props.removeCartCourse(data)}
    //     />
    //   ));
    // } else {
    //   // If the mode is completed courses, then we want to display the courses in the compact view.
    //   // Completed courses should allow the user to give the course a rating.
    if (this.props.mode === "completed") {
        console.log("entering completed mode")
        courses = this.props.data.map((course) => (
          <Course
            key={course.number}
            data={course}
            compactView={true}
            ratingMode={true}
            setRating={this.props.setRating}
          />
        ));
        return(
          <React.Fragment>
            <Container>
              {courses}
            </Container>
          </React.Fragment>
        )
    } 
    else{
      console.log("entering main")
          courses = this.props.data.map((course) => (
            <Course
              key={course.number}
              data={course}
              compactView={false}
              cartCourses={this.props.cartCourses}
              addCartCourse={this.props.addCartCourse}
              removeCartCourse={this.props.removeCartCourse}
              expandedCourse={true}
            />
          ));
          cart = this.props.cartCourses.map((course) => (
            <Course
              key={course.number}
              data={course}
              compactView={true}
              cartCourses={this.props.cartCourses}
              addCartCourse={this.props.addCartCourse}
              removeCartCourse={(data) => this.props.removeCartCourse(data)}
              expandedCourse={true}
            />
          ));
          if(cart.length === 0){
            return(
              <React.Fragment>
                <Container fluid>
                  <Row>
                    <Col sm={8}>
                      <div className="left-element"> 
                        <h1  class ="CartMessage">
                          Available Classes</h1>  
                        {courses}
                      </div>
                    </Col>
                    <Col sm={4}>
                      <div className="" class="right-element">
                        <h1  class ="CartMessage">
                        Your Cart is Empty. Add Courses to Enroll!</h1>  
                        {cart}
                      </div>
                    </Col>
                  </Row>
                </Container>
              </React.Fragment>
            )
          }
          else{
            return(
              <React.Fragment>
                <Container fluid>
                  <Row>
                    <Col sm={8}>
                      <div class="left-element"> 
                        <h1  class ="CartMessage">
                            Available Classes</h1>  
                        {courses}
                      </div>
                    </Col>
                    <Col sm={4}>
                      <div class="right-element">
                        <h1 class = "CartMessage">
                        Your Cart</h1>  
                        {cart}
                      </div>
                    </Col>
                  </Row>
                </Container>
              </React.Fragment>
            )
          }
          
        
      }

  }

  render() {
    return <div style={{ margin: "5px" }}>{this.getCourses()}</div>;
  }
}

export default CourseArea;
