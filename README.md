* Borrar tipo_herencia en onchange empleado *act_controla* = 154
* valor a mostra 





    def buscar_datos_erroneso(self, bienes):
        for b in bienes:
            if b[2]['dato_icorrecto']:
                raise ValidationError("Corregir los Bienes Marcados en ROJO")