$.getScript(base+"js/plugins/dataTables/datatables.min.js",function(){
    $.getScript(base+"js/personalizado/datatables/ajax_cache_pipeline_datatables.js", function(){
        $(document).ready(function () {

            // DEFINICIÓN DE LOS BOTONES PARA LA DATATABLE
            try{
                var custom_buttons = custom_buttons;
            }catch(err){
                var custom_buttons = null;
            }
            var final_buttons;
            if(custom_buttons){
                final_buttons = custom_buttons;
            }else{
                final_buttons = [
                    {
                        extend: 'copy',
                        exportOptions: {
                            columns: ':not(:last)'
                        },
                        text: 'Copiar'
                    },
                    {
                        extend: 'csv',
                        exportOptions: {
                            columns: ':not(:last)'
                        },
                        text: 'CSV'
                    },
                    {
                        extend: 'excel',
                        title: 'ListadoExportado',
                        exportOptions: {
                            columns: ':not(:last)'
                        },
                        text: 'Excel'
                    },
                    {
                        extend: 'pdf',
                        title: 'ListadoExportado',
                        exportOptions: {
                            columns: ':not(:last)'
                        },
                        text: 'PDF'
                    },

                    {
                        extend: 'print',
                        customize: function (win) {
                            $(win.document.body).addClass('white-bg');
                            $(win.document.body).css('font-size', '10px');

                            $(win.document.body).find('table')
                                .addClass('compact')
                                .css('font-size', 'inherit');
                        },
                        exportOptions: {
                            columns: ':not(:last)'
                        },
                        text: 'Imprimir'
                    }
                ]
            }
            // =========================================================================================================

            // DEFINICIÓN DE COLUMNAS
            var columns = column_defs;

            if(opciones){
                columns.push({"title": "Opciones", "targets": columns.length, "orderable": false, "searchable":false});
            }

            //==========================================================================================================

            var $table = $("#datatable-observatorio2").DataTable({
                dom: '<"html5buttons"B>lTr<"asyncsearch"f>gitp',
                language: {
                    "url": "//cdn.datatables.net/plug-ins/1.10.11/i18n/Spanish.json"
                },
                responsive: true,
                bAutoWidth: false,
                pageLength: 10,
                columnDefs: columns,
                serverSide: true,
                processing: true,
                ajax: $.fn.dataTable.pipeline({
                    url: "",
                    pages: 7 // number of pages to cache
                }),
                buttons: final_buttons

            });

            $(document).on( 'preInit.dt', function (e, settings) {
                var $input = $(".asyncsearch input");
                var $label = $input.closest("label");
                $label.html($input);
                var $button = $("<button class='btn btn-success btn-sm' >Buscar</button>").insertBefore($input);
                $button.css("margin-bottom", "0");

                $button.click(function(){
                    var val = $input.val();
                    $table.search(val).draw();
                });
            });
        });
    });
});