import React, { useState } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import postData from "../../services/httpFetch";

const FieldForm = (props) => {
  const { label, placeHolder, name, onChange } = props;
  return (
    <Form.Group controlId={`exampleForm.${name}`}>
      <Form.Label>{label}</Form.Label>
      <Form.Control
        as="input"
        placeholder={placeHolder ?? label}
        name={name}
        onChange={onChange}
      />
    </Form.Group>
  );
};

const FormCalcularNota = () => {
  const [formData, setFormData] = useState({
    proyecto1: 61,
    proyecto2: 61,
    proyecto3: 61,
    proyecto4: 61,
  });

  const onChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const calcularNota = () => {
    postData("/calcular-nota", formData)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.log("error", error));
  };

  return (
    <>
      <Row>
        <Col>
          <FieldForm
            name="proyecto1"
            label="Nota proyecto 1"
            placeHolder="Ingrese la nota del proyecto 1"
            onChange={onChange}
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <FieldForm
            name="proyecto2"
            label="Nota proyecto 2"
            placeHolder="Ingrese la nota del proyecto 2"
            onChange={onChange}
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <FieldForm
            name="proyecto3"
            label="Nota proyecto 3"
            placeHolder="Ingrese la nota del proyecto 3"
            onChange={onChange}
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <FieldForm
            name="proyecto4"
            label="Nota proyecto 4"
            placeHolder="Ingrese la nota del proyecto 4"
            onChange={onChange}
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <Button
            type="submit"
            className="btn btn-success"
            onClick={calcularNota}
          >
            Calcular Nota
          </Button>
        </Col>
      </Row>
    </>
  );
};

export default FormCalcularNota;
