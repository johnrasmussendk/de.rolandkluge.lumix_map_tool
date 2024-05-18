# Files larger than 50MB is not allowed using GitHub
# -- Ended using Google Driver instead

# Split files larger than 45MB into files of size 40MB, using split
# A larger file is splitted into smaller files with the same name
# and appended with '_split_'<two-digit-sequence-number>

# maptool.py merges the splitted files to one file

find panasonic-DMC-TZ30,DMC-TZ31,DMC-TZ27-cd-content -type f -print0 \
    | xargs -0 stat -c '%s %n' \
    | sort -n \
    | grep '4[5-9][0-9]\{6\} \|[5-9][0-9]\{7\} \|[0-9]\{9\} ' \
    | sed 's/^[0-9]\{8,\} //' \
    | while read FILE ; do
        echo "${FILE}"
	DIR_NAME="$(dirname "${FILE}")"
	DIR_DATE="$(stat -c '%y' "${DIR_NAME}")"
	DIR_PERMISSION="$(stat -c '%a' "${DIR_NAME}")"
	chmod +w "${DIR_NAME}" \
            && split -b 40000000 -a 2 -d "${FILE}" "${FILE}"'_split_' \
	    && for SPLIT_FILE in "${FILE}"'_split_'*; do
	           touch -r "${FILE}" "${SPLIT_FILE}" \
		       && chmod --reference="${FILE}" "${SPLIT_FILE}"
	       done \
	    && rm "${FILE}" \
	    && chmod "${DIR_PERMISSION}" "${DIR_NAME}" \
	    && touch -d "${DIR_DATE}" "${DIR_NAME}"
      done
