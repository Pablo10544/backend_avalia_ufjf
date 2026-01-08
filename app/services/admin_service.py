from app.repositories.admin_repository import AdminRepository

class AdminService:

    @staticmethod
    def deletar_comentario(avaliacao_id):
        if not avaliacao_id:
            raise ValueError("Avaliação inválida")

        avaliacao = AdminRepository.buscar_avaliacao(avaliacao_id)
        if not avaliacao:
            raise ValueError("Avaliação não encontrada")

        AdminRepository.remover_comentario(avaliacao)

    @staticmethod
    def aprovar_admin(id_pedido):
        if not id_pedido:
            raise ValueError("Pedido inválido")

        pedido = AdminRepository.buscar_pedido_admin(id_pedido)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        AdminRepository.aprovar_pedido(pedido)

    @staticmethod
    def deletar_todas_avaliacoes():
        AdminRepository.deletar_todas_avaliacoes()

    @staticmethod
    def deletar_docentes_sem_vinculo():
        AdminRepository.deletar_docentes_sem_vinculo()
