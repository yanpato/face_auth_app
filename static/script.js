/*
 * 認証関係のユーティリティ
 *
*/


/*
 * 登録か、loginかを選択してサーバーにリクエストを送る
*/
export function reqfunc(canvas, request_head) {
    const dataURL = canvas.toDataURL('image/png');
    return fetch('/upload', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
		request_head: request_head,
		image: dataURL 
	}),
    })
}

