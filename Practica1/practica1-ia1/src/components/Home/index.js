import React from "react";
import { Button, Card, Col, Container, Navbar, Row } from "react-bootstrap";
import FormFileLabel from "react-bootstrap/esm/FormFileLabel";
import FormCalcularNota from "../FormCalcularNota";
import FormModelo from "../FormModelo";

const Home = () => {
  return (
    <Container>
      <br />
      <Navbar expand="lg" variant="dark" bg="dark">
        <Navbar.Brand href="#">
          Practica 1 - Inteligencia Artificial 1 - Oscar Cuéllar - 201503712
        </Navbar.Brand>
      </Navbar>
      <Card>
        <Row>
          <Col lg="6">
            <Row>
              <Col lg="8">
                <div className="space">
                  <input
                    title="Seleccionar archivo"
                    type="file"
                    id="single"
                    accept=".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
                  />
                </div>
              </Col>
            </Row>
            <Row>
              <Col lg="8">
                <div className="marginCard">
                  <FormModelo />
                </div>
              </Col>
            </Row>
            <Row>
              <Col lg="8">
                <Button type="submit" className="btn btn-success">
                  Generar Modelo
                </Button>
              </Col>
            </Row>
          </Col>
          <Col lg="6">
            <div className="space">
              <FormCalcularNota />
            </div>
          </Col>
        </Row>
      </Card>
    </Container>
  );
};

export default Home;
