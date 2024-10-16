<script lang="ts">
	import { isUserLogged, rootData } from '$lib/stores';
	import EmojiSelector from '$lib/components/emojiSelector.svelte';
	import { showToast } from '$lib';

	export let post: any;
	export let imageOnly;
	export let showButtons = false;
	export let index = 0;
	export let showActions = false;
	export let useAnalytics = true;
	export let onlyDownload = false;
	let onScreen: boolean;
	export let width: number = 6440;
	export let height: number = 6440;
	let isEditMode: boolean = false;
	const addresses = $rootData.addresses;
	let postStyle = '';
	let loaded = false;
	let error: string;
	let buttonWidth: number;

	$: if (post.expand_image) {
		postStyle = get_post_size(true);
	} else {
		postStyle = get_post_size(false);
	}
	async function loadImage() {
		if (loaded) return;

		const img = new Image();
		img.src = `${$rootData.addresses.url}/posts/${post['source']}.jpg`;
		img.onload = () => {
			width = img.naturalWidth;
			height = img.naturalHeight;
			post.width = width;
			post.height = height;
			postStyle = get_post_size(false);
			loaded = true;
			if (useAnalytics) {
				if ($isUserLogged) {
					if ($rootData.user.info.admin) {
						return;
					}

					postViewed(
						post.id,
						$rootData.user.info.user_id,
						$rootData.user.info.firstname,
						$rootData.user.info.lastname
					);
				} else {
					postViewed(post.id);
				}
			}
		};
		img.onerror = (e) => {
			error = `Could not load post`;
		};
	}

	function get_post_size(full: boolean) {
		let size: string;

		if (full) {
			let newWidth = innerWidth - innerWidth / 8;
			let newHeight = (height * newWidth) / width;

			if (newHeight > innerHeight) {
				newHeight = innerHeight - innerHeight / 8;
				newWidth = (width * newHeight) / height;
			}

			size = `width: ${newWidth}px; height: ${newHeight}px;`;
		} else {
			// Set fixed height to 436px and calculate width accordingly
			let newWidth = (436 * width) / height;
			size = `width: ${newWidth}px; height: 436px;`;
		}

		return size;
	}

	async function delete_post(title: string, description: string, path: string, time: number) {
		try {
			const response = await fetch($rootData.addresses.delete, {
				method: 'POST',
				body: JSON.stringify({ title, description, path, time }),
				headers: {
					'Content-Type': 'application/json',
					'x-api-key': $rootData.apikey
				}
			});
			const updatedArray = $rootData.posts.filter(
				(item: { source: string }) => item.source !== path
			);
			$rootData.posts = updatedArray;
			return await response.json().then((data) => {
				showToast('Post deleted succesfully', data.status);
			});
		} catch (error) {
			showToast('Could not delete post: ' + error);
		}
	}

	async function edit_post(post_id: string, title: string, description: string) {
		try {
			const response = await fetch($rootData.addresses.edit_post, {
				method: 'POST',
				body: JSON.stringify({ post_id, title, description }),
				headers: {
					'Content-Type': 'application/json',
					'x-api-key': $rootData.apikey
				}
			});
			await response.json().then((data) => {
				showToast('Post edited succesfully', data.status);
			});
		} catch (error) {
			showToast('Could not edit post: ' + error);
		}
	}

	function toggleExpandImage(index: number) {
		$rootData.posts = $rootData.posts.map((post: { expand_image: any }, i: number) => {
			if (i === index) {
				return { ...post, expand_image: !post.expand_image };
			} else {
				return { ...post, expand_image: false };
			}
		});
	}
	let tmpReactions: (string | undefined)[] = [];
	let lastIndex: number;

	interface Reaction {
		user_id: string;
		emoji: string | undefined;
	}

	const like_address = addresses['like'];
	const unlike_address = addresses['unlike'];

	function toggleEmojiPicker(index: number | undefined) {
		$rootData.posts = $rootData.posts.map((post: { expand_picker: any }, i: number) => {
			if (i === index) {
				return { ...post, expand_picker: !post.expand_picker };
			} else {
				return { ...post, expand_picker: false };
			}
		});
		if (index != undefined) {
			lastIndex = index;
		}
	}

	async function likePost(post_id: string) {
		const user_id = $rootData.user.info.user_id;
		const like_id = user_id + post_id;

		if (!$rootData.user.liked_posts.some((like: { post_id: string }) => like.post_id === post_id)) {
			addLike(post_id);
			$rootData.user.liked_posts = [...$rootData.user.liked_posts, { like_id, user_id, post_id }];

			try {
				const response = await fetch(like_address, {
					method: 'POST',
					body: JSON.stringify({ post_id, user_id }),
					headers: {
						'Content-Type': 'application/json'
					}
				});
				await response.json();
			} catch (error) {
				showToast('Could not like post: ' + error);
			}
		} else {
			// console.log('Post already liked');
		}
	}

	async function unlikePost(post_id: string) {
		const user_id = $rootData.user.info.user_id;

		if ($rootData.user.liked_posts.some((like: { post_id: string }) => like.post_id === post_id)) {
			delLike(post_id);
			$rootData.user.liked_posts = $rootData.user.liked_posts.filter(
				(like: { post_id: string }) => like.post_id !== post_id
			);

			try {
				const response = await fetch(unlike_address, {
					method: 'POST',
					body: JSON.stringify({ post_id, user_id }),
					headers: {
						'Content-Type': 'application/json'
					}
				});
				await response.json();
			} catch (error) {
				console.error('Could not unlike post: ', error);
			}
		}
	}

	function addLike(post_id: string) {
		const index = $rootData.posts.findIndex((post: { id: string }) => post.id === post_id);
		if (index !== -1) {
			$rootData.posts[index].like_count += 1;
		}
	}

	function delLike(post_id: string) {
		const index = $rootData.posts.findIndex((post: { id: string }) => post.id === post_id);
		if (index !== -1) {
			$rootData.posts[index].like_count -= 1;
		}
	}

	async function removeReaction(emoji: string | undefined) {
		const user_id = $rootData.user.info.user_id;
		try {
			const response = await fetch($rootData.addresses.unreact, {
				method: 'POST',
				body: JSON.stringify({ user_id, emoji }),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			await response.json();
		} catch (error) {
			console.error('Could not remove reaction from post');
		}
	}

	let checkReactionUser = (reaction: { user_id?: string }) => {
		return reaction.user_id == $rootData.user.info.user_id ? true : false;
	};

	function prioritizeUserId(reactions: Reaction[], userIdToPrioritize: string) {
		if (Object.keys($rootData.user.reacted_posts).length > 0) {
			return reactions.sort((a, b) => {
				if (a.user_id === userIdToPrioritize) return -1;
				if (b.user_id === userIdToPrioritize) return 1;
				return 0;
			});
		} else {
			return $rootData.user.reacted_posts;
		}
	}

	let hasUserLiked = (post: { id: string }) => {
		if (Object.keys($rootData.user.liked_posts).length > 0) {
			return $rootData.user.liked_posts.some(
				(like: { post_id: string }) => like.post_id == post.id
			);
		} else {
			false;
		}
	};

	let hasUserReacted = (post: { reactions: [] }) => {
		if (Object.keys($rootData.user.reacted_posts).length > 0) {
			return post.reactions.some(
				(reaction: { user_id: any }) => reaction.user_id == $rootData.user.info.user_id
			);
		} else {
			false;
		}
	};

	function actionWhenInViewport(e: any) {
		const observer = new IntersectionObserver((entries) => {
			if (entries[0].isIntersecting) {
				onScreen = true;
				loadImage();
			}
		});

		observer.observe(e);
	}

	async function postViewed(
		post_id: string,
		user_id: string | undefined = undefined,
		firstname: string | undefined = undefined,
		lastname: string | undefined = undefined
	) {
		try {
			const response = await fetch($rootData.addresses.url + '/api/post/' + post_id + '/view', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ post_id, user_id, firstname, lastname })
			});
			await response.json();
		} catch (error) {
			console.error('Could not remove reaction from post');
		}
	}

	let addReaction: HTMLElement;
	let x: number;
	function getElementCoordinates(addReaction: HTMLElement) {
		const rect = addReaction.getBoundingClientRect();
		x = rect.left + window.scrollX;
	}
</script>

{#if loaded}
	{#if imageOnly}
		<img
			src={`${$rootData.addresses.url}/posts/${post['source']}.jpg`}
			class="radius-medium"
			alt="post"
		/>
	{:else}
		<div
			class="post {post.id} shadow space-between flexcolumn radius-heavy"
			class:fullscreen_post={post.expand_image}
			style="background-image: url('{$rootData.addresses.url}/posts/{post[
				'source'
			]}.jpg'); {postStyle}"
		>
			<div class="top fit-height space-between radius-medium flexrow">
				<div class="title">
					{#if isEditMode}
						<input class="input-title" type="text" bind:value={post.name} />
					{:else}
						<h2 style="margin: 0; margin-top: 0.5rem;">{post['name']}</h2>
						{#if post.views_count === 0}
							<small>0 <i class="fa-solid fa-eye"></i></small>
						{:else}
							<small>{post.views_count} <i class="fa-solid fa-eye"></i></small>
						{/if}
					{/if}
				</div>
				{#if showButtons}
					<div class="actions fit-content">
						{#if !onlyDownload}
							<button id="enlarge_btn" on:click={() => toggleExpandImage(index)}
								><i
									class="fa-solid"
									class:fa-up-right-and-down-left-from-center={!post.expand_image}
									class:fa-down-left-and-up-right-to-center={post.expand_image}
								></i></button
							>
						{/if}
						<a
							href="{$rootData.addresses.url}/posts/{post['source']}.jpg"
							download={post['source']}
							class="button"
							id="download"
							rel="external"
						>
							<i class="fa-solid fa-download"></i>
						</a>

						{#if $isUserLogged && !onlyDownload}
							{#if $rootData.user.info.admin}
								{#if isEditMode}
									<button
										id="apply"
										class="button"
										on:click={() => {
											isEditMode = !isEditMode;
											edit_post(post.id, post.name, post.description);
										}}
									>
										<i class="fa-solid fa-check"></i>
									</button>
								{:else}
									<button
										id="edit"
										class="button"
										on:click={() => {
											isEditMode = !isEditMode;
										}}
									>
										<i class="fa-solid fa-pen-to-square"></i>
									</button>
								{/if}
								<button
									id="trash"
									class="button errorbackground"
									on:click={async () => {
										const result = await delete_post(
											post.name,
											post.description,
											post.source,
											post.time
										);
									}}
								>
									<i class="fa-solid fa-trash"></i>
								</button>
							{/if}
						{/if}
					</div>
				{/if}
			</div>
			<div class="description">
				{#if isEditMode}
					<input type="text" bind:value={post.description} class="input-description" />
				{:else}
					<p>{post.description}</p>
				{/if}
			</div>
		</div>
		{#if showActions}
			<div class="post-actions flexcolumn">
				<div class="top">
					<div class="likes-wrapper">
						{#if $isUserLogged}
							{#if hasUserLiked(post)}
								<button
									class="transparent"
									on:click={() => {
										unlikePost(post.id);
									}}
								>
									<i class="fa-solid fa-heart icon like-icon liked"></i>
								</button>
							{:else}
								<button
									class="transparent"
									on:click={() => {
										likePost(post.id);
									}}
								>
									<i class="fa-regular fa-heart icon like-icon"></i>
								</button>
							{/if}
						{:else}
							<button
								class="transparent"
								on:click={() => {
									showToast('Log in to like posts', 300);
								}}
							>
								<i class="fa-regular fa-heart icon like-icon"></i>
							</button>
						{/if}
						{#if post.like_count === 1}
							<p>{post.like_count} Like</p>
						{:else}
							<p>{post.like_count} Likes</p>
						{/if}
					</div>
					<div class="reaction-wrapper valign">
						{#if $isUserLogged}
							{#if (!tmpReactions[index] && !hasUserReacted(post)) || tmpReactions[index] == undefined}
								<button
									bind:this={addReaction}
									bind:clientWidth={buttonWidth}
									class="fa-solid fa-circle-plus soft border-soft add-reaction flexrow fit-content valign"
									on:click={() => {
										getElementCoordinates(addReaction);
										toggleEmojiPicker(index);
									}}><p style="transform: translateY(2px);">Add reaction</p></button
								>
							{:else if tmpReactions[index]}
								<p class="reaction border-soft my-reaction circle" style="padding: 0;">
									{tmpReactions[index]}
								</p>
								<button
									class="fa-solid fa-circle-minus soft border-soft flexrow fit-content valign"
									on:click={() => {
										removeReaction(tmpReactions[index]);
										tmpReactions[index] = undefined;
									}}><p>Remove reaction</p></button
								>
							{/if}

							{#each prioritizeUserId(post.reactions, $rootData.user.info.user_id) as reaction}
								{#if !checkReactionUser(reaction)}
									<p class="reaction border-soft circle" style="padding: 0;">{reaction.emoji}</p>
								{:else if checkReactionUser(reaction) && reaction.emoji}
									<p class="reaction border-soft circle my-reaction" style="padding: 0;">
										{reaction.emoji}
									</p>
									<button
										class="fa-solid fa-circle-minus soft border-soft flexrow fit-content valign"
										on:click={() => {
											removeReaction(reaction.emoji);
											reaction.emoji = undefined;
											tmpReactions[index] = undefined;
										}}><p>Remove reaction</p></button
									>
								{/if}
							{/each}
						{:else if Object.values(post.reactions).length != 0}
							{#each post.reactions as reaction}
								<p class="reaction border-soft circle" style="padding: 0;">{reaction.emoji}</p>
							{/each}
						{/if}
					</div>
					<EmojiSelector
						bind:post_id={post.id}
						bind:showPicker={post.expand_picker}
						bind:emoji={tmpReactions[index]}
						bind:x
						bind:buttonWidth
					></EmojiSelector>
				</div>
			</div>
		{/if}
	{/if}
{:else if error}
	<div class="placeholder radius-heavy error errorfont halign valign">
		{error} <button on:click={loadImage}><i class="fa-solid fa-rotate-right"></i></button>
	</div>
{:else}
	<div
		use:actionWhenInViewport
		class="placeholder radius-heavy"
		class:bottommargin={showActions}
	></div>
{/if}

<style>
	p {
		margin: 0 !important;
	}
	.error {
		font-size: 1.5rem;
		gap: 1rem;
	}
	.bottommargin {
		margin-bottom: 4rem;
	}
	.placeholder {
		max-width: 100% !important;
		background: linear-gradient(135deg, rgba(0, 0, 0, 0) 0%, rgba(62, 62, 62, 1) 100%);
		background-size: 250% 250%;
		animation: loading 3s infinite;
		transition-timing-function: cubic-bezier(0.3, 0.7, 1, 0.1);
		width: 42rem;
		height: 27.5rem;
	}

	@keyframes loading {
		0% {
			background-position: 33% 50%;
		}
		50% {
			background-position: 66% 50%;
		}
		100% {
			background-position: 33% 50%;
		}
	}

	.input-description {
		width: 75%;
	}
	.input-title {
		font-size: 1.5rem;
		width: 100% !important;
		padding: 0;
	}
	.post p,
	.post h2,
	.post small,
	.post .fa-eye {
		color: #e5e2df;
	}
	img {
		display: block;
		max-width: 40vw;
		max-height: 320px;
		width: auto;
		height: auto;
		object-fit: scale-down;
	}
	.post {
		border: 2px solid var(--border-color);
		padding: 1rem;
		max-width: calc(100% - 2rem) !important;
		background-position: center; /* Center the image */
		background-size: cover; /* or contain */
	}
	.post > .top {
		background-color: var(--background-blurry);
		backdrop-filter: blur(2.5px);
		padding: 0.5rem;
		padding-left: 1rem;
		padding-right: 1rem;
		text-align: left;
	}
	.post > .top > .title {
		text-align: left;
		min-width: unset !important;
	}
	.post > .description {
		line-height: 1.25rem;
		text-align: center !important;
	}
	#download {
		max-height: 16px;
		width: 16px;
	}
	.add-reaction {
		margin-right: 0.5rem !important;
	}
	.soft {
		padding: 0.25rem;
		background-color: var(--background-blurry);
		gap: 0.5rem;
	}
	.reaction {
		display: unset !important;
		flex-direction: row;
		padding: 0.25rem !important;
		background-color: var(--background-blurry);
		gap: 0.5rem;
		font-size: 1rem;
		height: 1rem;
	}
	.reaction-wrapper {
		height: 24px;
		font-size: 1.5rem;
		gap: 0.5rem;
	}
	.reaction-wrapper p {
		max-height: 24px;
	}
	.post-actions > .top {
		display: flex;
		flex-direction: row;
		gap: 1rem;
		margin: 0.5rem;
	}
	.likes-wrapper {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 0.5rem;
	}
	.like-icon:hover {
		scale: 110%;
	}
	.like-icon:active,
	.liked {
		scale: 100%;
		color: red;
	}
	@media screen and (max-width: 1000px) {
		.fullscreen_post {
			transition-duration: 0s !important;
		}
	}
	@media screen and (max-width: 720px) {
		.placeholder {
			height: 24rem;
		}
		.fullscreen_post {
			border: none;
			border-radius: unset;
			position: fixed !important;
			z-index: 10;
			background-size: contain !important;
			background-repeat: no-repeat !important;
			background-color: var(--background-blurry);
			backdrop-filter: blur(20px);
			top: 0px !important;
			left: 0px !important;
			min-width: 100vw !important;
			height: 100vh !important;
			padding: 0 !important;
		}
		.fullscreen_post > .top {
			backdrop-filter: unset;
			background-color: transparent;
			margin: unset;
			margin-top: 1rem !important;
		}
		.fullscreen_post > .description {
			visibility: hidden;
		}
	}
</style>
