import React, { useState } from "react";
import { Button, Col, Form, Row } from "react-bootstrap";
import postData from "../../services/httpFetch";

const dataFinalizacion = [
  { id: "generacion", label: "Máximo número de generaciones - 1k" },
  {
    id: "promedio",
    label: "Valor fitness promedio dentro de la población - 0.40",
  },
  {
    id: "fitness",
    label: "Fitness mínimo alcanzado por una solución - 0.40",
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
  const { data, label, onChange, name } = props;

  return (
    <>
      <Form.Group controlId="exampleForm.ControlSelect1">
        <Form.Label>{label}</Form.Label>
        <Form.Control as="select" onChange={onChange} name={name}>
          {data.map((x) => (
            <option value={x?.id}>{x?.label}</option>
          ))}
        </Form.Control>
      </Form.Group>
    </>
  );
};

const FormModelo = () => {
  const [formData, setFormData] = useState({
    finalizacion: "generacion",
    padres: "aleatoria",
  });

  const onChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const generarModelo = () => {
    postData("/generar-modelo", formData)
      .then((response) => response.text())
      .then((result) => console.log(result))
      .catch((error) => console.log("error", error));
  };

  return (
    <>
      <Select
        data={dataFinalizacion}
        label="Seleccionar criterio de finalización"
        name="finalizacion"
        onChange={onChange}
      />
      <Select
        data={dataSeleccionPadres}
        label="Seleccionar criterio de selección de padres"
        name="padres"
        onChange={onChange}
      />
      <Button type="submit" className="btn btn-success" onClick={generarModelo}>
        Generar Modelo
      </Button>
    </>
  );
};

export default FormModelo;
