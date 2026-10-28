import flet as ft


def main(page: ft.Page):
    # Configuración general de la página
    page.title = "Portal de Autogestión Institucional"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # AppBar institucional
    page.appbar = ft.AppBar(
        title=ft.Text("Portal de Autogestión Educativa", weight=ft.FontWeight.BOLD),
        center_title=False,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        actions=[
            ft.IconButton(ft.Icons.NOTIFICATIONS_NONE, tooltip="Notificaciones"),
            ft.IconButton(ft.Icons.ACCOUNT_CIRCLE, tooltip="Perfil de Usuario"),
        ]
    )

    # --- PESTAÑA 1: Fechas de Examen ---
    examenes_data = [
        {"materia": "Programación II", "fecha": "12/11/2026", "hora": "19:00 hs", "aula": "Laboratorio 3"},
        {"materia": "Bases de Datos Relacionales", "fecha": "15/11/2026", "hora": "20:00 hs", "aula": "Aula 102"},
        {"materia": "Lógica Proposicional", "fecha": "18/11/2026", "hora": "19:30 hs", "aula": "Aula Magna"},
    ]

    examenes_cards = []
    for ex in examenes_data:
        examenes_cards.append(
            ft.Card(
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Text(ex["materia"], size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Divider(),
                        ft.Row([
                            ft.Icon(ft.Icons.CALENDAR_MONTH, size=18, color=ft.Colors.BLUE_600),
                            ft.Text(f"Fecha: {ex['fecha']}"),
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.ACCESS_TIME, size=18, color=ft.Colors.BLUE_600),
                            ft.Text(f"Horario: {ex['hora']}"),
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.LOCATION_ON, size=18, color=ft.Colors.BLUE_600),
                            ft.Text(f"Lugar: {ex['aula']}"),
                        ]),
                    ], spacing=8)
                )
            )
        )

    tab_examenes = ft.Container(
        padding=10,
        content=ft.Column([
            ft.Text("Próximas Fechas de Exámenes Finales", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Consulte las fechas de sus exámenes programados para el presente turno.",
                    color=ft.Colors.GREY_700),
            ft.Column(examenes_cards, spacing=10)
        ], spacing=15)
    )

    # --- PESTAÑA 2: Estado de Trámites ---
    tramites_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("N° Trámite")),
            ft.DataColumn(ft.Text("Tipo de Trámite")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Estado")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("#TR-2026-089")),
                ft.DataCell(ft.Text("Solicitud de Analítico Parcial")),
                ft.DataCell(ft.Text("05/10/2026")),
                ft.DataCell(ft.Container(
                    content=ft.Text("En Proceso", color=ft.Colors.WHITE, size=12),
                    bgcolor=ft.Colors.ORANGE_600,
                    padding=5,
                    border_radius=5
                )),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("#TR-2026-042")),
                ft.DataCell(ft.Text("Constancia de Alumno Regular")),
                ft.DataCell(ft.Text("12/09/2026")),
                ft.DataCell(ft.Container(
                    content=ft.Text("Aprobado", color=ft.Colors.WHITE, size=12),
                    bgcolor=ft.Colors.GREEN_600,
                    padding=5,
                    border_radius=5
                )),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("#TR-2026-011")),
                ft.DataCell(ft.Text("Homologación de Materia")),
                ft.DataCell(ft.Text("01/08/2026")),
                ft.DataCell(ft.Container(
                    content=ft.Text("Finalizado", color=ft.Colors.WHITE, size=12),
                    bgcolor=ft.Colors.BLUE_600,
                    padding=5,
                    border_radius=5
                )),
            ]),
        ]
    )

    tab_tramites = ft.Container(
        padding=10,
        content=ft.Column([
            ft.Text("Seguimiento de Trámites", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Estado en tiempo real de sus solicitudes administrativas.", color=ft.Colors.GREY_700),
            ft.ResponsiveRow([
                ft.Container(content=tramites_table, padding=10)
            ])
        ], spacing=15)
    )

    # --- PESTAÑA 3: Solicitud de Turnos ---
    txt_nombre = ft.TextField(label="Nombre y Apellido", icon=ft.Icons.PERSON)
    txt_dni = ft.TextField(label="DNI / Documento", keyboard_type=ft.KeyboardType.NUMBER, icon=ft.Icons.BADGE)

    # Dropdown adaptado sin el parámetro 'icon' que generaba problemas en versiones recientes
    dd_motivo = ft.Dropdown(
        label="Motivo de la consulta",
        options=[
            ft.dropdown.Option("Secretaría Académica"),
            ft.dropdown.Option("Tesorería / Aranceles"),
            ft.dropdown.Option("Orientación Estudiantil"),
            ft.dropdown.Option("Mesa de Entradas"),
        ]
    )
    txt_fecha = ft.TextField(label="Fecha preferida (DD/MM/AAAA)", icon=ft.Icons.CALENDAR_TODAY)

    def confirmar_turno(e):
        if not txt_nombre.value or not txt_dni.value or not dd_motivo.value or not txt_fecha.value:
            dlg = ft.AlertDialog(
                title=ft.Text("Campos Incompletos"),
                content=ft.Text("Por favor completa todos los campos requerired."),
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            return

        dlg_exito = ft.AlertDialog(
            title=ft.Text("¡Turno Reservado con Éxito!"),
            content=ft.Text(
                f"Estimado/a {txt_nombre.value}, su turno para {dd_motivo.value} el día {txt_fecha.value} ha sido registrado."),
            actions=[
                ft.TextButton("Aceptar", on_click=lambda _: close_dialog())
            ]
        )

        def close_dialog():
            dlg_exito.open = False
            page.update()

        page.dialog = dlg_exito
        dlg_exito.open = True
        page.update()
        # Limpiar formulario
        txt_nombre.value = ""
        txt_dni.value = ""
        dd_motivo.value = None
        txt_fecha.value = ""
        page.update()

    # Botón principal actualizado a ft.FilledButton propio de Flet 1.0+
    btn_solicitar = ft.FilledButton(
        content=ft.Row([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.WHITE),
            ft.Text("Confirmar Reserva de Turno", color=ft.Colors.WHITE)
        ], tight=True),
        bgcolor=ft.Colors.BLUE_700,
        on_click=confirmar_turno
    )

    tab_turnos = ft.Container(
        padding=10,
        content=ft.Column([
            ft.Text("Reserva de Turno Administrativo", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Complete el formulario para solicitar atención presencial o virtual.", color=ft.Colors.GREY_700),
            txt_nombre,
            txt_dni,
            dd_motivo,
            txt_fecha,
            ft.Container(height=10),
            btn_solicitar
        ], spacing=15, width=600)
    )

    # --- Estructura Principal con Pestañas ---
    content_area = ft.Container(content=tab_examenes, expand=True)

    def cambiar_pestana(e):
        for btn in [btn1, btn2, btn3]:
            btn.style = ft.ButtonStyle(color=ft.Colors.BLUE_700)
        e.control.style = ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700)
        idx = int(e.control.data)
        if idx == 0:
            content_area.content = tab_examenes
        elif idx == 1:
            content_area.content = tab_tramites
        elif idx == 2:
            content_area.content = tab_turnos
        page.update()

    btn1 = ft.TextButton("Fechas de Examen", data="0", on_click=cambiar_pestana, style=ft.ButtonStyle(color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_700))
    btn2 = ft.TextButton("Mis Trámites", data="1", on_click=cambiar_pestana, style=ft.ButtonStyle(color=ft.Colors.BLUE_700))
    btn3 = ft.TextButton("Solicitar Turno", data="2", on_click=cambiar_pestana, style=ft.ButtonStyle(color=ft.Colors.BLUE_700))

    barra_pestanas = ft.Row([btn1, btn2, btn3], spacing=5)
    page.add(ft.Column([barra_pestanas, content_area], expand=True))


if __name__ == "__main__":
    ft.run(main)