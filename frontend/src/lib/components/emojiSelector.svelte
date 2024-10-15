<script lang="ts">
	import { rootData } from '$lib/stores';

	let emojiList = [
		{ emoji: '😀', keyword: 'smile happy joy' },
		{ emoji: '😃', keyword: 'happy joy grin' },
		{ emoji: '😄', keyword: 'grin smile joy' },
		{ emoji: '😁', keyword: 'smile teeth grin' },
		{ emoji: '😆', keyword: 'laugh smile happy' },
		{ emoji: '😅', keyword: 'sweat smile relieved' },
		{ emoji: '😂', keyword: 'tears joy laughing' },
		{ emoji: '🤣', keyword: 'rofl rolling laugh' },
		{ emoji: '🥲', keyword: 'smile tear bittersweet' },
		{ emoji: '🥹', keyword: 'tears grateful touched' },
		{ emoji: '😊', keyword: 'smile blush happy' },
		{ emoji: '😇', keyword: 'angel innocent' },
		{ emoji: '🙂', keyword: 'smile content' },
		{ emoji: '🙃', keyword: 'upside down silly' },
		{ emoji: '😉', keyword: 'wink smile flirty' },
		{ emoji: '😌', keyword: 'relieved calm' },
		{ emoji: '😍', keyword: 'heart eyes love' },
		{ emoji: '🥰', keyword: 'in love happy' },
		{ emoji: '😘', keyword: 'kiss flirty love' },
		{ emoji: '😗', keyword: 'kiss happy' },
		{ emoji: '😙', keyword: 'kiss smile happy' },
		{ emoji: '😚', keyword: 'kiss closed eyes' },
		{ emoji: '😋', keyword: 'yum tasty' },
		{ emoji: '😛', keyword: 'tongue playful' },
		{ emoji: '😝', keyword: 'tongue closed eyes' },
		{ emoji: '😜', keyword: 'wink tongue' },
		{ emoji: '🤪', keyword: 'crazy silly' },
		{ emoji: '🤨', keyword: 'raised eyebrow skeptical' },
		{ emoji: '🧐', keyword: 'monocle curious' },
		{ emoji: '🤓', keyword: 'nerd glasses geek' },
		{ emoji: '😎', keyword: 'cool sunglasses' },
		{ emoji: '🥸', keyword: 'disguise funny' },
		{ emoji: '🤩', keyword: 'star eyes excited' },
		{ emoji: '🥳', keyword: 'party celebration' },
		{ emoji: '😏', keyword: 'smirk smug' },
		{ emoji: '😒', keyword: 'unimpressed discontent' },
		{ emoji: '😞', keyword: 'sad disappointed' },
		{ emoji: '😔', keyword: 'sad pensive' },
		{ emoji: '😟', keyword: 'worried concerned' },
		{ emoji: '😕', keyword: 'confused unsure' },
		{ emoji: '🙁', keyword: 'frown sad' },
		{ emoji: '☹️', keyword: 'frown upset' },
		{ emoji: '😣', keyword: 'persevering stressed' },
		{ emoji: '😖', keyword: 'confounded frustrated' },
		{ emoji: '😫', keyword: 'tired exhausted' },
		{ emoji: '😩', keyword: 'weary drained' },
		{ emoji: '🥺', keyword: 'pleading puppy eyes' },
		{ emoji: '😢', keyword: 'cry sad tears' },
		{ emoji: '😭', keyword: 'sob tears crying' },
		{ emoji: '😮‍💨', keyword: 'relief exhale' },
		{ emoji: '😤', keyword: 'triumph proud' },
		{ emoji: '😠', keyword: 'angry mad' },
		{ emoji: '😡', keyword: 'rage furious' },
		{ emoji: '🤬', keyword: 'cursing angry swearing' },
		{ emoji: '🤯', keyword: 'mind blown shocked' },
		{ emoji: '😳', keyword: 'flushed surprised embarrassed' },
		{ emoji: '🥵', keyword: 'hot sweating' },
		{ emoji: '🥶', keyword: 'cold freezing' },
		{ emoji: '😱', keyword: 'scream scared' },
		{ emoji: '😨', keyword: 'fearful scared' },
		{ emoji: '😰', keyword: 'anxious worried sweat' },
		{ emoji: '😥', keyword: 'sad relieved disappointed' },
		{ emoji: '😓', keyword: 'sweat disappointed' },
		{ emoji: '🫣', keyword: 'peeking embarrassed' },
		{ emoji: '🤗', keyword: 'hugging warm' },
		{ emoji: '🫡', keyword: 'salute respect' },
		{ emoji: '🤔', keyword: 'thinking curious' },
		{ emoji: '🫢', keyword: 'oops shock' },
		{ emoji: '🤭', keyword: 'hand over mouth surprise' },
		{ emoji: '🤫', keyword: 'shush quiet' },
		{ emoji: '🤥', keyword: 'lying nose' },
		{ emoji: '😶', keyword: 'speechless quiet' },
		{ emoji: '😶‍🌫️', keyword: 'foggy confused' },
		{ emoji: '😐', keyword: 'neutral indifferent' },
		{ emoji: '😑', keyword: 'expressionless blank' },
		{ emoji: '😬', keyword: 'grimace awkward' },
		{ emoji: '🫨', keyword: 'shaking shock' },
		{ emoji: '🫠', keyword: 'melting embarrassed' },
		{ emoji: '🙄', keyword: 'eyeroll annoyed' },
		{ emoji: '😯', keyword: 'surprised hushed' },
		{ emoji: '😦', keyword: 'frowning surprised' },
		{ emoji: '😧', keyword: 'anguished shocked' },
		{ emoji: '😮', keyword: 'open mouth surprised' },
		{ emoji: '😲', keyword: 'astonished surprised' },
		{ emoji: '🥱', keyword: 'yawn tired' },
		{ emoji: '😴', keyword: 'sleeping tired' },
		{ emoji: '🤤', keyword: 'drooling sleepy' },
		{ emoji: '😪', keyword: 'sleepy tired' },
		{ emoji: '😵', keyword: 'dizzy confused' },
		{ emoji: '😵‍💫', keyword: 'dizzy disoriented' },
		{ emoji: '🫥', keyword: 'disguised hidden' },
		{ emoji: '🤐', keyword: 'zipper mouth quiet' },
		{ emoji: '🥴', keyword: 'woozy drunk' },
		{ emoji: '🤢', keyword: 'nauseated sick' },
		{ emoji: '🤮', keyword: 'vomit sick' },
		{ emoji: '🤧', keyword: 'sneezing sick' },
		{ emoji: '😷', keyword: 'mask sick' },
		{ emoji: '🤒', keyword: 'fever thermometer' },
		{ emoji: '🤕', keyword: 'hurt head bandage' },
		{ emoji: '🤑', keyword: 'money greedy' },
		{ emoji: '🤠', keyword: 'cowboy hat happy' },
		{ emoji: '😈', keyword: 'devil smiling evil' },
		{ emoji: '👿', keyword: 'angry devil' },
		{ emoji: '👹', keyword: 'ogre monster' },
		{ emoji: '👺', keyword: 'goblin mask' },
		{ emoji: '🤡', keyword: 'clown silly' },
		{ emoji: '💩', keyword: 'poop funny' },
		{ emoji: '👻', keyword: 'ghost spooky' },
		{ emoji: '💀', keyword: 'skull dead' },
		{ emoji: '☠️', keyword: 'skull crossbones' },
		{ emoji: '👽', keyword: 'alien extraterrestrial' },
		{ emoji: '👾', keyword: 'space invader alien' },
		{ emoji: '🎃', keyword: 'pumpkin halloween' },
		{ emoji: '😺', keyword: 'smile cat' },
		{ emoji: '😸', keyword: 'grinning cat' },
		{ emoji: '😹', keyword: 'tears joy cat' },
		{ emoji: '😻', keyword: 'heart eyes cat' },
		{ emoji: '😼', keyword: 'smirk cat' },
		{ emoji: '😽', keyword: 'kiss cat' },
		{ emoji: '🙀', keyword: 'scared shocked cat' },
		{ emoji: '😿', keyword: 'crying sad cat' },
		{ emoji: '😾', keyword: 'angry cat' },
		{ emoji: '👋', keyword: 'wave hello' },
		{ emoji: '🤚', keyword: 'raised hand stop' },
		{ emoji: '✋', keyword: 'raised hand high five' },
		{ emoji: '🖖', keyword: 'vulcan salute star trek' },
		{ emoji: '👌', keyword: 'ok hand gesture' },
		{ emoji: '🤌', keyword: 'pinched fingers italian gesture' },
		{ emoji: '🤏', keyword: 'pinching small' },
		{ emoji: '✌️', keyword: 'peace victory' },
		{ emoji: '🤞', keyword: 'fingers crossed hope' },
		{ emoji: '🫰', keyword: 'finger heart love' },
		{ emoji: '🤟', keyword: 'love you sign' },
		{ emoji: '🤘', keyword: 'rock horns metal' },
		{ emoji: '🤙', keyword: 'call me hang loose' },
		{ emoji: '🫵', keyword: 'you pointing' },
		{ emoji: '🫱', keyword: 'palm facing right' },
		{ emoji: '🫲', keyword: 'palm facing left' },
		{ emoji: '🫸', keyword: 'pushing hand right' },
		{ emoji: '🫷', keyword: 'pushing hand left' },
		{ emoji: '🫳', keyword: 'hand holding down' },
		{ emoji: '🫴', keyword: 'hand holding up' },
		{ emoji: '👈', keyword: 'point left' },
		{ emoji: '👉', keyword: 'point right' },
		{ emoji: '👆', keyword: 'point up' },
		{ emoji: '🖕', keyword: 'middle finger rude' },
		{ emoji: '👇', keyword: 'point down' },
		{ emoji: '☝️', keyword: 'pointing up finger' },
		{ emoji: '👍', keyword: 'thumbs up approval' },
		{ emoji: '👎', keyword: 'thumbs down disapproval' },
		{ emoji: '✊', keyword: 'raised fist power' },
		{ emoji: '👊', keyword: 'fist bump punch' },
		{ emoji: '🤛', keyword: 'left facing fist bump' },
		{ emoji: '🤜', keyword: 'right facing fist bump' },
		{ emoji: '👏', keyword: 'clap applause' },
		{ emoji: '🫶', keyword: 'heart hands love' },
		{ emoji: '🙌', keyword: 'raised hands celebration' },
		{ emoji: '👐', keyword: 'open hands give' },
		{ emoji: '🤲', keyword: 'palms together offering' },
		{ emoji: '🤝', keyword: 'handshake agreement' },
		{ emoji: '🙏', keyword: 'praying hands thanks' }
	];

	export let showPicker = false;
	export let emoji = '';
	export let post_id = '';
	export let x: number;
	export let buttonWidth: number;

	let searchString: string = '';
	let filteredEmojis = [...emojiList];

	function searchEmoji() {
		searchString = searchString.toLowerCase();
		filteredEmojis = emojiList.filter(({ keyword }) =>
			keyword.toLowerCase().includes(searchString)
		);
	}

	async function addReaction(post_id: string) {
		const user_id = $rootData.user.info.user_id;
		try {
			const response = await fetch($rootData.addresses.react, {
				method: 'POST',
				body: JSON.stringify({ user_id, post_id, emoji }),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			const result = await response.json();
		} catch (error) {
			console.error('Could not react to post');
		}
	}

	let innerWidth: number;
	let innerHeight: number;
	let dialog: HTMLDialogElement;

	let tmpWidth: number | undefined;
	let move: number = 0;
	let style: string;

	$: if (innerWidth) {
		if (tmpWidth === undefined) {
			tmpWidth = innerWidth;
		}
		if (innerWidth > 720 && innerWidth < 1000) {
			style = 'left: 75px';
		} else if (innerWidth < 720) {
			style = 'left: 30px';
		} else if (innerWidth > 1000) {
			move = (innerWidth - tmpWidth) / 2;
			style = `left: ${Math.round(x - 336 / 2) + buttonWidth / 2 + move}px;`;
		}
	}
</script>

<svelte:window bind:innerWidth bind:innerHeight />

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore missing-declaration -->
<!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
<div
	class="close_area"
	class:show={showPicker}
	on:click|stopPropagation={(e) => {
		// @ts-ignore
		if (!dialog.contains(e.target)) {
			showPicker = false;
		}
	}}
></div>

<dialog class="root outline" class:show={showPicker} bind:this={dialog} {style}>
	<input
		type="text"
		bind:value={searchString}
		on:input={() => {
			searchEmoji();
		}}
		placeholder="Search emojis..."
	/>
	<div class="selector">
		{#each filteredEmojis as row}
			<button
				class="transparent"
				on:click={() => {
					emoji = row.emoji;
					showPicker = !showPicker;
					addReaction(post_id);
				}}><p>{row.emoji}</p></button
			>
		{/each}
	</div>
</dialog>

<style>
	.close_area {
		width: 100vw;
		height: 100vh;
		background-color: transparent;
		display: none;
		position: fixed;
		left: 0px;
		top: 0px;
	}
	.root {
		transform: translateY(2rem);
		transition-duration: 0s !important;
		z-index: 10;
		position: absolute;
		display: none;
		width: 300px;
		height: 400px;
		gap: 1rem;
		background-color: var(--background-blurry);
		border-radius: var(--border-radius-heavy);
		margin: 0 !important;
		overflow-x: hidden;
		overflow-y: scroll;
		flex-direction: column;
		backdrop-filter: blur(10px);
		border: 2px solid var(--border-color);
	}
	.selector {
		overflow-x: hidden;
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		font-size: 2rem;
		border-radius: var(--border-radius-heavy);
		gap: 0.5rem;
		text-align: center;
		justify-content: center;
	}
	.show {
		display: flex;
	}
	p {
		margin: 0 !important;
	}
	button {
		font-size: 2rem;
	}
</style>
