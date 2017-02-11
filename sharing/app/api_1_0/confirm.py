


@api.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('auth.login'))
    if current_user.confirm(token):
        flash('你的账户已被确认,谢谢')
    else :
        flash('确认链接无效或过期')
    return redirect(url_for('auth.login'))