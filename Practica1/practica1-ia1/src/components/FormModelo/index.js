import React from "react";
import {} from "bootstrap";
import { Col, Form, Row } from "react-bootstrap";

const dataFinalizacion = [
  { id: "generacion", label: "Máximo número de generaciones - 10000" },
  {
    id: "promedio",
    label: "Valor fitness promedio dentro de la población - 15",
  },
  {
    id: "fitness",
    label: "Fitness máximo alcanzado por una solución - 10",
  },
];

const dataSeleccionPadres = [
  { id: "aleatoria", label: "Selección de padres aleatoria" },
  {
    id: "impares",
    label: "Selección de padres en posiciones impar",
  },
  {
    id: "pares",
    label: "Selección de padres en posiciones pares",
  },
  {
    id: "fitness",
    label: "Selección de padres con mejor valor fitness",
  },
];

const Select = (props) => {
  const { data, label } = props;

  return (
    <>
      <Form.Group controlId="exampleForm.ControlSelect1">
        <Form.Label>{label}</Form.Label>
        <Form.Control as="select">
          {data.map((x) => (
            <option value={x?.id}>{x?.label}</option>
          ))}
        </Form.Control>
      </Form.Group>
    </>
  );
};

const FormModelo = () => {
  return (
    <>
      <Select
        data={dataFinalizacion}
        label="Seleccionar criterio de finalización"
      />
      <Select
        data={dataSeleccionPadres}
        label="Seleccionar criterio de selección de padres"
      />
    </>
  );
};

export default FormModelo;
