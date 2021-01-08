import React, { useState } from "react";
import { Button, Col, Form, FormLabel, Row } from "react-bootstrap";
import postData from "../../services/httpFetch";

const dataGenero = [
  { id: "1", label: "MASCULINO" },
  { id: "0", label: "FEMENINO" },
];

const dataDepartamentos = [
  { id: "1", label: "Guatemala" },
  { id: "2", label: "El progreso" },
  { id: "3", label: "Sacatepequez" },
  { id: "4", label: "Chimaltenango" },
  { id: "5", label: "Escuintla" },
  { id: "6", label: "Santa Rosa" },
  { id: "7", label: "Sololá" },
  { id: "8", label: "Totonicapán" },
  { id: "9", label: "Quetzaltenango" },
  { id: "10", label: "Suchitepequez" },
  { id: "11", label: "Retalhuleu" },
  { id: "12", label: "San Marcos" },
  { id: "13", label: "Huehuetenango" },
  { id: "14", label: "Quiché" },
  { id: "15", label: "Baja verapaz" },
  { id: "16", label: "Alta verapaz" },
  { id: "17", label: "Petén" },
  { id: "18", label: "Izabal" },
  { id: "19", label: "Zacapa" },
  { id: "20", label: "Chiquimula" },
  { id: "21", label: "Jalapa" },
  { id: "22", label: "Jutiapa" },
];

const dataMunicipios = [
  { id: "11", label: "Acatenango" },
  { id: "4", label: "Agua Blanca" },
  { id: "63", label: "Amatitlan" },
  { id: "1", label: "Antigua Guatemala" },
  { id: "5", label: "Asuncion Mita" },
  { id: "7", label: "Atescatempa" },
  { id: "2", label: "Barberena" },
  { id: "7", label: "CabaÃ±as" },
  { id: "5", label: "Camotan" },
  { id: "14", label: "Cantel" },
  { id: "16", label: "Catarina" },
  { id: "1", label: "Chimaltenango" },
  { id: "55", label: "Chinautla" },
  { id: "1", label: "Chiquimula" },
  { id: "8", label: "Chiquimulilla" },
  { id: "1", label: "Ciudad de Guatemala" },
  { id: "12", label: "Ciudad Vieja" },
  { id: "20", label: "Coatepeque" },
  { id: "1", label: "Coban" },
  { id: "4", label: "Comalapa" },
  { id: "11", label: "Comalapa" },
  { id: "4", label: "Cubulco" },
  { id: "1", label: "Cuilapa" },
  { id: "16", label: "El Tejar" },
  { id: "1", label: "Escuintla" },
  { id: "7", label: "Esquipulas" },
  { id: "2", label: "Estanzuela" },
  { id: "1", label: "Flores" },
  { id: "62", label: "Fraijanes" },
  { id: "15", label: "Fray Bartolome de las Casas" },
  { id: "21", label: "Genova" },
  { id: "4", label: "Gualan" },
  { id: "1", label: "Guastatoya" },
  { id: "1", label: "Huehuetenango" },
  { id: "11", label: "Ipala" },
  { id: "19", label: "Ixcan" },
  { id: "23", label: "Ixchiguan" },
  { id: "7", label: "Jacaltenango" },
  { id: "1", label: "Jalapa" },
  { id: "12", label: "Jalpatagua" },
  { id: "8", label: "Jerez" },
  { id: "4", label: "Jocotan" },
  { id: "2", label: "Jocotan" },
  { id: "12", label: "Joyabaj" },
  { id: "1", label: "Jutiapa" },
  { id: "10", label: "Magdalena Milpas Altas" },
  { id: "15", label: "Malacatan" },
  { id: "1", label: "Mazatenango" },
  { id: "57", label: "Mixco" },
  { id: "14", label: "Moyuta" },
  { id: "13", label: "Nueva Concepcion" },
  { id: "18", label: "Ocos" },
  { id: "6", label: "Oratorio" },
  { id: "54", label: "Palencia" },
  { id: "11", label: "Palin" },
  { id: "10", label: "Panajachel" },
  { id: "14", label: "Parramos" },
  { id: "3", label: "Pastores" },
  { id: "14", label: "Patulul" },
  { id: "9", label: "Patzicia" },
  { id: "7", label: "Patzun" },
  { id: "12", label: "Poptun" },
  { id: "13", label: "Pueblo Nuevo ViÃ±as" },
  { id: "1", label: "Puerto Barrios" },
  { id: "9", label: "Puerto de San Jose" },
  { id: "1", label: "Quetzaltenango" },
  { id: "3", label: "Rabinal" },
  { id: "1", label: "Retalhuleu" },
  { id: "3", label: "Rio Hondo" },
  { id: "1", label: "Salama" },
  { id: "2", label: "Salcaja" },
  { id: "13", label: "San Andres Itzapa" },
  { id: "15", label: "San Antonio Aguas Calientes" },
  { id: "8", label: "San Antonio La Paz" },
  { id: "10", label: "San Antonio Suchitepequez" },
  { id: "7", label: "San Bartolome Milpas Altas" },
  { id: "3", label: "San Benito" },
  { id: "4", label: "San Carlos Sija" },
  { id: "5", label: "San Felipe Retalhuleu" },
  { id: "6", label: "San Francisco" },
  { id: "3", label: "San Francisco El Alto" },
  { id: "53", label: "San Jose del Golfo" },
  { id: "52", label: "San Jose Pinula" },
  { id: "14", label: "San Juan Alotenango" },
  { id: "11", label: "San Juan Cotzal" },
  { id: "59", label: "San Juan Sacatepequez" },
  { id: "7", label: "San Lorenzo" },
  { id: "8", label: "San Lucas Sacatepequez" },
  { id: "13", label: "San Lucas Toliman" },
  { id: "3", label: "San Luis Jilotepeque" },
  { id: "1", label: "San Marcos" },
  { id: "4", label: "San MartÃ­n Zapotitlan" },
  { id: "3", label: "San Martin Jilotepeque" },
  { id: "13", label: "San Martin Jilotepeque" },
  { id: "66", label: "San Miguel Petapa" },
  { id: "56", label: "San Pedro Ayampuc" },
  { id: "9", label: "San Pedro Carcha" },
  { id: "58", label: "San Pedro Sacatepequez" },
  { id: "2", label: "San Pedro Sacatepequez" },
  { id: "12", label: "San Pedro Yepocapa" },
  { id: "60", label: "San Raymundo" },
  { id: "2", label: "San Sebastian" },
  { id: "12", label: "San Vicente Pacaya" },
  { id: "7", label: "Sanarate" },
  { id: "5", label: "Santa Apolonia" },
  { id: "51", label: "Santa Catarina Pinula" },
  { id: "10", label: "Santa Cruz Balanya" },
  { id: "1", label: "Santa Cruz del Quiche" },
  { id: "12", label: "Santa Cruz Naranjo" },
  { id: "2", label: "Santa Cruz Verapaz" },
  { id: "2", label: "Santa LucÃ­a Cotzumalguapa" },
  { id: "9", label: "Santa LucÃ­a Milpas Altas" },
  { id: "11", label: "Santa Maria de Jesus" },
  { id: "10", label: "Santa Maria Ixhuatan" },
  { id: "13", label: "Santa Maria Nebaj" },
  { id: "3", label: "Santa Rosa de Lima" },
  { id: "19", label: "Santiago Atitlan" },
  { id: "6", label: "Santiago Sacatepequez" },
  { id: "5", label: "Santo Domingo Xenacoj" },
  { id: "6", label: "Santo Tomas Chichicastenango" },
  { id: "1", label: "Solola" },
  { id: "4", label: "Sumpango" },
  { id: "9", label: "Taxisco" },
  { id: "6", label: "Tecpan Guatemala" },
  { id: "5", label: "Teculutan" },
  { id: "6", label: "Tiquisate" },
  { id: "1", label: "Totonicapan" },
  { id: "65", label: "Villa Canales" },
  { id: "64", label: "Villa Nueva" },
  { id: "1", label: "Zacapa" },
  { id: "4", label: "Zacualpa" },
  { id: "15", label: "Zaragoza" },
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

const TextBox = (props) => {
  const { label, defaultValue, name, disabled, readOnly, onChange } = props;

  return (
    <Form.Group>
      <FormLabel>{label}</FormLabel>
      <Form.Control
        type="text"
        value={defaultValue}
        name={name}
        disabled={disabled}
        readOnly={readOnly}
        onChange={onChange}
      />
    </Form.Group>
  );
};

const FormModelo = () => {
  const [formData, setFormData] = useState({
    genero: "1",
    departamento: "1",
    municipio: "1",
  });

  const [resultado, setResultado] = useState("");

  const onChange = (event) => {
    setFormData({ ...formData, [event.target.name]: event.target.value });
  };

  const generarModelo = () => {
    formData.distancia = 2;
    postData("/predecir", formData)
      .then((response) => response.json())
      .then((result) => {
        console.log(result);
        setResultado(result.response);
      })
      .catch((error) => console.log("error", error));
  };

  return (
    <>
      <Row>
        <Col lg="6">
          <Select
            data={dataGenero}
            label="Seleccionar Género"
            name="genero"
            onChange={onChange}
          />
        </Col>
        <Col lg="6">
          <TextBox name="edad" onChange={onChange} label="Edad" />
        </Col>
      </Row>
      <Row>
        <Col lg="6">
          <TextBox name="anio" onChange={onChange} label="Año de inscripción" />
        </Col>
        <Col lg="6">
          <Select
            data={dataDepartamentos}
            label="Departamento"
            name="departamento"
            onChange={onChange}
          />
        </Col>
      </Row>
      <Row>
        <Col lg="6">
          <Select
            data={dataMunicipios}
            label="Municipio"
            name="departamento"
            onChange={onChange}
          />
        </Col>
      </Row>
      <Row>
        <Col>
          <Button
            type="submit"
            className="btn btn-success"
            onClick={generarModelo}
          >
            Consultar
          </Button>
        </Col>
      </Row>
      <Row></Row>
      <Row>
        <Col lg="12">
          <TextBox
            name="resultado"
            defaultValue={resultado}
            label="Resultado predecido"
          />
        </Col>
      </Row>
    </>
  );
};

export default FormModelo;
