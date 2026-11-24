# 02 — UNIVERSIDAD / TECNO_BYTE

## Qué era el trabajo

Diseñar dos bases en MySQL desde cero: una para gestión universitaria y otra para una tienda de tecnología. No fueron ejercicios de `SELECT`. El punto fue que el esquema aguantara datos reales: alumnos, inscripciones, calificaciones, empleados, productos, ventas e inventario.

## Cómo lo armé

Primero normalicé hasta 3FN. Separé entidades y quité dependencias transitivas antes de escribir procedures. Después vine con los JOIN para los reportes: promedio por alumno, ventas por producto, stock crítico. `GROUP BY`, `HAVING`, subconsultas. Nada de traer toda la tabla y filtrar en la app.

Donde más cuidado puse fue en los objetos de base de datos:

- **Vistas** para no repetir el mismo JOIN cinco veces en reportes distintos.
- **Procedures** para operaciones de varias tablas: inscribir alumno, registrar venta, actualizar inventario.
- **Triggers** para validar antes de que entrara un dato malo.
- **GRANT / REVOKE** para que un usuario de consulta no pudiera borrar inventario.
- **`START TRANSACTION` / `COMMIT` / `ROLLBACK`** en ventas: si falla el descuento de stock, no queda la venta a medias.

También puse índices en las columnas que más se filtraban. No a todas, porque indexar por indexar solo gasta espacio y hace más lento el INSERT.

## Cómo lo pienso hoy

La parte difícil no fue escribir SQL. Fue decidir la granularidad de cada tabla y cuándo una normalización estricta empieza a cobrar caro en joins. Un trigger de validación no es lo mismo que un `CHECK`; el trigger puede tocar otras tablas, el `CHECK` no. Ese tipo de decisión es la que me interesa defender.

Lo que sí sé explicar sin apuntes: por qué una venta necesita transacción, cómo evito registros huérfanos y qué índice conviene crear según el query.

## Lo que no va en esta carpeta

No metí el dump `.sql`. No está en las máquinas que revisé y no voy a inventar un archivo para que el portafolio se vea más lleno. Si me lo piden, lo escribo y lo corro en MySQL enfrente de quien lo revise.

La ficha dice lo que hice; el código se entrega aparte cuando se solicite. Esa es la diferencia entre un portafolio armado y uno inventado.

## Preguntas que me harían y mi respuesta corta

- **¿Por qué 3FN y no BCNF?** Porque en estos esquemas 3FN resolvía la redundancia sin partir tablas hasta volverlas inmanejables.
- **¿Trigger o validación en la app?** Los dos cuando es crítico. El trigger es la última línea de defensa aunque alguien entre directo a MySQL.
- **¿Qué pasa si el COMMIT falla?** Se hace ROLLBACK. Stock y venta quedan como estaban. Ese es el punto de ACID.

No me quedo en el `SELECT`. Si el trigger no dispara o la transacción se rompe, me quedo hasta encontrar la causa. Eso me gusta.
