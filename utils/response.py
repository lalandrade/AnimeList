from flask import jsonify

def success(message, data=None, status=200):
    """
    Retorna resposta de sucesso padronizada
    
    Args:
        message: Mensagem de sucesso
        data: Dados opcionais (dict, list, etc)
        status: Código HTTP (padrão 200)
    
    Retorna:
        JSON: {"success": True, "message": "...", "data": ...}
    """
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status


def error(message, status=400):
    """
    Retorna resposta de erro padronizada
    
    Args:
        message: Mensagem de erro
        status: Código HTTP (padrão 400)
    
    Retorna:
        JSON: {"success": False, "message": "...", "data": null}
    """
    return jsonify({
        "success": False,
        "message": message,
        "data": None
    }), status
