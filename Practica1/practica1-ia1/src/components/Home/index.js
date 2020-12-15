import React from "react";
import { Button, Card, Col, Container, Navbar, Row } from "react-bootstrap";
import FormCalcularNota from "../FormCalcularNota";
import FormModelo from "../FormModelo";
import postData from "./../../services/httpFetch";

const Home = () => {
  const parsearArchivo = (event) => {
    const f = event.target.files[0];
    if (f) {
      var r = new FileReader();
      r.onload = function (e) {
        var ct = r.result;
        const rows = ct.split("\n");
        crearJSONObject(rows, f);
      };
      r.readAsText(f);
    } else {
      alert("Failed to load file");
    }
  };

  const crearJSONObject = (rows, file) => {
    let jsonObject = { data: [], nombreDoc: file.name };

    rows.forEach((row, index) => {
      const columns = row.split(",");
      if (index > 0) {
        jsonObject.data.push({
          proyecto1: columns[0],
          proyecto2: columns[1],
          proyecto3: columns[2],
          proyecto4: columns[3],
          notaReal: columns[4],
        });
      }
    });

    postData("/data-excel", jsonObject)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.log("error", error));
  };

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
                    onChange={parsearArchivo}
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
