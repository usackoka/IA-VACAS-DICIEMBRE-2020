import React from "react";
import { Card, Col, Container, Navbar, Row } from "react-bootstrap";
import { LazyLoadImage } from "react-lazy-load-image-component";
import postData from "./../../services/httpFetch";

const Home = () => {
  const parsearArchivo = (event) => {
    return;
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
          Practica 2 - Inteligencia Artificial 1 - Oscar Cuéllar - 201503712
        </Navbar.Brand>
      </Navbar>
      <Card>
        <Row>
          <Col lg="12">
            <Row>
              <Col lg="11">
                <div className="space">
                  <input
                    onChange={parsearArchivo}
                    title="Seleccionar imagenes"
                    multiple
                    type="file"
                    id="single"
                  />
                </div>
              </Col>
            </Row>
            <Row>
              <Col lg="1" />
              <Col lg="10">
                <div className="marginCard">
                  <div>
                    <LazyLoadImage
                      alt={"name"}
                      height={128}
                      width={128}
                      src="./../../../public/logo512.png" // use normal <img> attributes as props
                    />
                    <span>{"name"}</span>
                  </div>
                </div>
              </Col>
            </Row>
          </Col>
        </Row>
      </Card>
    </Container>
  );
};

export default Home;
