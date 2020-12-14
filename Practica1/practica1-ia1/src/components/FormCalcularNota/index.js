import React from "react";
import { Button, Col, Form, Row } from "react-bootstrap";

const FieldForm = (props) => {
  const { label, placeHolder, name } = props;
  return (
    <Form.Group controlId={`exampleForm.${name}`}>
      <Form.Label>{label}</Form.Label>
      <Form.Control as="input" placeholder={placeHolder ?? label} name={name} />
    </Form.Group>
  );
};

const FormCalcularNota = () => {
  return (
    <>
      <Row>
        <Col>
          <FieldForm
            name="proyecto1"
            label="Nota proyecto 1"
            placeHolder="Ingrese la nota del proyecto 1"
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <FieldForm
            name="proyecto2"
            label="Nota proyecto 2"
            placeHolder="Ingrese la nota del proyecto 2"
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <FieldForm
            name="proyecto3"
            label="Nota proyecto 3"
            placeHolder="Ingrese la nota del proyecto 3"
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <FieldForm
            name="proyecto4"
            label="Nota proyecto 4"
            placeHolder="Ingrese la nota del proyecto 4"
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <Button type="submit" className="btn btn-success">
            Calcular Nota
          </Button>
        </Col>
      </Row>
    </>
  );
};

export default FormCalcularNota;
