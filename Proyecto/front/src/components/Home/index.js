import React from "react";
import { Card, Col, Container, Navbar, Row } from "react-bootstrap";
import FormModelo from "../FormModelo";

const Home = () => {
  return (
    <Container>
      <br />
      <Navbar expand="lg" variant="dark" bg="dark">
        <Navbar.Brand href="#">
          Proyecto - Inteligencia Artificial 1 - Oscar Cuéllar - 201503712
        </Navbar.Brand>
      </Navbar>
      <Card>
        <Row>
          <Col lg="12">
            <div className="marginCard">
              <FormModelo />
            </div>
          </Col>
        </Row>
      </Card>
    </Container>
  );
};

export default Home;
