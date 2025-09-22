-- FILE: import.sql

-- Marcas
INSERT INTO core_marca VALUES (1, 'Total');
INSERT INTO core_marca VALUES (2, 'Hyundai');
INSERT INTO core_marca VALUES (3, 'Stanley');
INSERT INTO core_marca VALUES (4, 'Grau');
INSERT INTO core_marca VALUES (5, 'Arauco');
INSERT INTO core_marca VALUES (6, 'Bash');
INSERT INTO core_marca VALUES (7, 'Veloti');
INSERT INTO core_marca VALUES (8, 'Mamut');
INSERT INTO core_marca VALUES (9, 'Arar');
INSERT INTO core_marca VALUES (10, 'Imporper');
INSERT INTO core_marca VALUES (11, 'Tajamar');
INSERT INTO core_marca VALUES (12, 'Sipa');
INSERT INTO core_marca VALUES (13, 'Bosch');

-- Tipo de Productos
INSERT INTO core_tipoproducto VALUES (1, 'Herramientas Manuales');
INSERT INTO core_tipoproducto VALUES (2, 'Materiales Básicos');
INSERT INTO core_tipoproducto VALUES (3, 'Equipos de Seguridad');
INSERT INTO core_tipoproducto VALUES (4, 'Tornillos y Anclajes');
INSERT INTO core_tipoproducto VALUES (5, 'Fijaciones y Adhesivos');
INSERT INTO core_tipoproducto VALUES (6, 'Equipos de Medición');

-- Productos
INSERT INTO core_producto VALUES(1,'Taladro de impacto 13 mm 680W TG1061356 Total','El taladro de impacto TG1061356 de Total ofrece una potencia de entrada de 680W, una velocidad sin carga de 0 - 3000 RPM y una capacidad máxima de perforación de 13 mm. También, cuenta con velocidad variable, interruptor de avance y retroceso y función de martillo.',29990,5,'https://www.ferremax.cl/storage/2021/06/TG10613362.jpg',1,1);
INSERT INTO core_producto VALUES(2,'Lijadora orbital 240W SS24-B2C Stanley','No aplica',35990,3,'https://www.easy.cl/_next/image?url=https%3A%2F%2Feasycl.vteximg.com.br%2Farquivos%2Fids%2F4973300%2F1279178-0000-002.jpg%3Fv%3D638742015721200000&w=640&q=75',3,1);
INSERT INTO core_producto VALUES(3,'Destornillador punta cruz PH2 100 mm Cushion Grip Stanley','El Destornillador Cushion Grip de Stanley cuenta con punta imantada, que facilita el encaje de la punta en el tornillo, mango con diseño innovador, que se diferencia por la excelente ergonomía y óptimo manejo, y punta endurecida para una vida útil más larga. Además, tiene identificación de la medida en la parte superior de la herramienta y un orificio en el mango para facilitar el almacenaje.',9990,10,'https://www.easy.cl/_next/image?url=https%3A%2F%2Feasycl.vteximg.com.br%2Farquivos%2Fids%2F5053531%2F1250815-0000-001.jpg%3Fv%3D638743266730930000&w=750&q=75',3,1);
INSERT INTO core_producto VALUES(4,'Pino seco cepillado premium 1x2 3,2 m','Pino seco 12 Pulgadas 3,2 mt',1390,20,'https://www.easy.cl/_next/image?url=https%3A%2F%2Feasycl.vteximg.com.br%2Farquivos%2Fids%2F4337527%2F192591-0000-001.jpg%3Fv%3D638727432517900000&w=640&q=75',5,2);
INSERT INTO core_producto VALUES(5,'Pino seco cepillado premium 1x8 3,2 m','Pino seco 1. 8 Pulgadas 3,2 Metros',5990,10,'https://www.easy.cl/_next/image?url=https%3A%2F%2Feasycl.vteximg.com.br%2Farquivos%2Fids%2F4337527%2F192591-0000-001.jpg%3Fv%3D638727432517900000&w=640&q=75',5,2);
-- ... (and so on for all other products)

-- Estado Pedido
INSERT INTO core_estadopedido (estado) VALUES ('Pendiente');
INSERT INTO core_estadopedido (estado) VALUES ('En revision');
INSERT INTO core_estadopedido (estado) VALUES ('Confirmado');
INSERT INTO core_estadopedido (estado) VALUES ('Rechazado');
INSERT INTO core_estadopedido (estado) VALUES ('En proceso');
INSERT INTO core_estadopedido (estado) VALUES ('Enviado');
INSERT INTO core_estadopedido (estado) VALUES ('Cancelado');

-- Estado Entrega
INSERT INTO core_estadoentrega (estado) VALUES ('En espera');
INSERT INTO core_estadoentrega (estado) VALUES ('Confirmado');
INSERT INTO core_estadoentrega (estado) VALUES ('Cancelado');