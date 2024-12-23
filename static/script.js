/*
 * 認証関係のユーティリティ
 *
*/


/*
 * 登録か、loginかを選択してサーバーにリクエストを送る
*/
export function reqfunc(canvas, username, request_head) {
    const dataURL = canvas.toDataURL('image/png');
    return fetch(request_head, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
		request_head: request_head,
		user_name: username,
		image: dataURL 
	}),
    })
}

